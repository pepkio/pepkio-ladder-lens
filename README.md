# Ladder Lens

Quantitative gel electrophoresis band size estimation and molecular weight calibration tool utilizing semi-log regression and dual-ladder gel smile correction.

# Overview

In molecular biology, biochemistry, and genomics, gel electrophoresis is standard practice for separating nucleic acid fragments (DNA and RNA) and proteins based on charge, size, and conformation. Determining the exact length of DNA/RNA fragments in base pairs (bp) or the molecular weight of proteins in kilodaltons (kDa) from gel images requires constructing a calibration curve using standard molecular weight markers (ladders).

Manual size estimation—whether performed by visual inspection against an adjacent ladder or by manual measurement with a physical ruler—is subjective, labor-intensive, and prone to measurement error. Non-uniform electrophoresis conditions, such as thermal gradients across agarose or polyacrylamide gels, frequently induce a "smile effect" where migration velocity varies across lanes.

Ladder Lens automates gel band sizing by calculating relative migration distance ($R_f$), constructing semi-log standard curves ($\log_{10}(\text{size})$ vs. $R_f$), and applying dual-ladder interpolation algorithms to compensate for gel smile distortion. The tool provides coefficient of determination ($R^2$) diagnostic feedback, boundary extrapolation warnings, and standardized methods text for academic publications.

Ladder Lens is available as an open-source Python package on GitHub (https://github.com/pepkio/pepkio-ladder-lens) and as an interactive web application (https://www.pepkio.com/tools/ladder-lens).

# Features

- **Semi-Log Linear & Polynomial Regression**: Fits logarithmic molecular weight ($\log_{10}(\text{size})$) against relative mobility ($R_f$) to compute precise standard curve parameters.
- **Dual-Ladder Gel Smile Correction**: Interpolates migration curves across left and right reference ladders to compensate for thermal distortion and edge-effect curvature.
- **Automated Relative Mobility ($R_f$) Calculation**: Converts pixel migration coordinates ($y_{\text{well}}$, $y_{\text{front}}$, $y_{\text{band}}$) into normalized mobility values ($0.0$ to $1.0$).
- **Goodness-of-Fit Diagnostics**: Calculates $R^2$ values and residual standard error to validate standard curve accuracy.
- **Extrapolation & Boundary Safeguards**: Identifies unknown sample bands migrating outside the calibrated ladder boundaries and issues diagnostic warnings.
- **Flexible Molecular Units**: Supports DNA/RNA fragment sizing (base pairs, bp; kilobases, kb) and protein mass determination (kilodaltons, kDa).
- **Methods Text Generator**: Automatically generates standardized scientific methodology prose detailing regression parameters for research manuscripts and lab notebooks.

# Common Use Cases

- **PCR Amplicon Verification**: Sizing PCR products against 100 bp or 1 kb DNA ladders to confirm specific target amplification before downstream cloning or sequencing.
- **Restriction Fragment Length Analysis**: Estimating fragment lengths following restriction enzyme digestion to verify plasmid construction and recombinant clones.
- **SDS-PAGE Protein Mass Determination**: Estimating target protein molecular mass (kDa) against pre-stained protein standards after purification.
- **CRISPR/Cas9 Cleavage Assays**: Sizing parent DNA and cleavage product bands to evaluate guide RNA (gRNA) cleavage efficiency.
- **NGS Library QC**: Checking fragment length distribution of sheared genomic DNA or cDNA libraries prior to high-throughput sequencing.
- **RNA Integrity Assessment**: Estimating sizes of in vitro transcribed RNA or total RNA fractions on denaturing agarose gels.

# Why This Tool Exists

Manual estimation of gel bands from digital images or printed films introduces several technical challenges:

1. **Manual Spreadsheet Limitations**: Spreadsheets require manual log transformation of ladder sizes and linear regression modeling. Manual entry is error-prone and lacks automated validation of migration range or curve fit quality.
2. **Visual Inspection Error**: Subjective comparison against adjacent ladder lanes typically yields size estimates with $\pm 10-20\%$ error, particularly for fragments migrating between non-linearly spaced ladder bands.
3. **Gel Smile Distortion**: Temperature gradients across agarose or polyacrylamide gels cause central lanes to migrate faster or slower than outer lanes. Single-ladder calibration curves fail to account for this horizontal migration bias.
4. **Lack of Reproducible Documentation**: Physical ruler measurements or basic image annotators lack standardized audit trails, coordinate archiving, and reproducible methods generation required for rigorous scientific reporting.

Ladder Lens addresses these limitations by providing programmatic calculation of relative mobility, dual-ladder spatial correction, rigorous statistical curve fitting, and structured output.

# Installation

The official Python client for Ladder Lens is hosted on PyPI (https://pypi.org/project/pepkio-ladder-lens/).

Install the package via `pip`:

```bash
pip install pepkio-ladder-lens
```

### Requirements

- Python >= 3.11
- Dependencies: `click`, `httpx`, `pydantic`

# Quick Start

### Single-Ladder Calibration Example

```python
from pepkio_ladder_lens import PepkioClient

# Initialize client (API key can also be set via PEPKIO_API_KEY environment variable)
client = PepkioClient(api_key="your_api_key_here")

# Define ladder markers and unknown sample migration coordinates (y-pixels)
input_data = {
    "unit": "bp",
    "fit_model": "semi_log_linear",
    "ladder_mode": "single",
    "ladder_name": "NEB 1 kb DNA Ladder",
    "y_well": 40,
    "y_front": 400,
    "ladder_bands": [
        {"label": "10 kb", "known_size": 10000, "migration_y": 95},
        {"label": "8 kb", "known_size": 8000, "migration_y": 110},
        {"label": "6 kb", "known_size": 6000, "migration_y": 125},
        {"label": "5 kb", "known_size": 5000, "migration_y": 135},
        {"label": "4 kb", "known_size": 4000, "migration_y": 150},
        {"label": "3 kb", "known_size": 3000, "migration_y": 170},
        {"label": "2 kb", "known_size": 2000, "migration_y": 200},
        {"label": "1.5 kb", "known_size": 1500, "migration_y": 225},
        {"label": "1 kb", "known_size": 1000, "migration_y": 260},
        {"label": "0.5 kb", "known_size": 500, "migration_y": 320},
    ],
    "sample_bands": [
        {"label": "PCR Amplicon - Lane 2", "migration_y": 215},
        {"label": "Digest Fragment - Lane 3", "migration_y": 165},
    ],
}

# Run sizing estimation
result = client.run(input_data)

print(f"Fit Model: {result.result['fit']['model']}")
print(f"Fit R²: {result.result['fit']['r_squared']}")

for sample in result.result["samples"]:
    print(f"{sample['label']}: {sample['estimated_size_display']} (Rf: {sample['rf']:.3f})")
```

### Dual-Ladder Smile Correction Example

```python
# Compensate for gel smile using reference ladders on both flanks of the gel
dual_ladder_input = {
    "unit": "bp",
    "fit_model": "semi_log_linear",
    "ladder_mode": "dual",
    "y_well": 40,
    "y_front": 400,
    "left_ladder_bands": [
        {"label": "L_10kb", "known_size": 10000, "migration_y": 98},
        {"label": "L_3kb", "known_size": 3000, "migration_y": 173},
        {"label": "L_1kb", "known_size": 1000, "migration_y": 263},
    ],
    "right_ladder_bands": [
        {"label": "R_10kb", "known_size": 10000, "migration_y": 92},
        {"label": "R_3kb", "known_size": 3000, "migration_y": 167},
        {"label": "R_1kb", "known_size": 1000, "migration_y": 257},
    ],
    "sample_bands": [
        {"label": "Center Lane Sample", "migration_y": 170, "lane_position_x": 0.5},
    ],
}

result_dual = client.run(dual_ladder_input)
print("Dual-Ladder Sizing Result:")
for sample in result_dual.result["samples"]:
    print(f"{sample['label']}: {sample['estimated_size_display']}")
```

### Command-Line Interface (CLI)

```bash
export PEPKIO_API_KEY="your_api_key_here"

# Display available pre-configured examples
pepkio-ladder-lens manifest --examples

# Run a standard gel sizing calculation
pepkio-ladder-lens run --example neb_1kb_single_ladder
```

# Example Output

Running a standard gel band estimation returns structured JSON containing calibration metrics, sample predictions, warnings, and publication-ready methods text:

```json
{
  "run_id": "run_9a8b7c6d5e",
  "status": "completed",
  "result": {
    "fit": {
      "model": "semi_log_linear",
      "r_squared": 0.9982,
      "slope": -3.8421,
      "intercept": 4.5120
    },
    "ladder_points": [
      {"label": "10 kb", "rf": 0.1528, "log10_mw": 4.0000, "known_size": 10000},
      {"label": "3 kb", "rf": 0.3611, "log10_mw": 3.4771, "known_size": 3000},
      {"label": "1 kb", "rf": 0.6111, "log10_mw": 3.0000, "known_size": 1000}
    ],
    "samples": [
      {
        "label": "PCR Amplicon - Lane 2",
        "migration_y": 215,
        "rf": 0.4861,
        "estimated_size": 1403.4,
        "estimated_size_display": "1403 bp",
        "status": "ok"
      },
      {
        "label": "Digest Fragment - Lane 3",
        "migration_y": 165,
        "rf": 0.3472,
        "estimated_size": 3788.1,
        "estimated_size_display": "3788 bp",
        "status": "ok"
      }
    ],
    "warnings": [],
    "methods_text": "Band sizes were estimated by semi-log linear regression of log10(molecular size) against relative migration distance (Rf). Relative mobility was calculated as Rf = (y_band - y_well) / (y_front - y_well). Standard curve calibration achieved R² = 0.9982 across 10 ladder standards."
  },
  "permalink": "https://tools.pepkio.com/r/run_9a8b7c6d5e"
}
```

# Scientific Background

### Principles of Gel Electrophoresis Separation

Gel electrophoresis separates charged biomolecules in an electric field ($E$) forced through a porous gel matrix (e.g., agarose or polyacrylamide).

Under an applied potential difference, biomolecules migrate toward the electrode of opposite charge. For nucleic acids, the uniform negative charge-to-mass ratio imparted by the phosphate backbone results in migration velocity being determined by sieving through the gel matrix. Smaller fragments move through matrix pores with less resistance, migrating further than larger fragments.

### Relative Migration Distance ($R_f$)

To normalize band migration across different gels, run times, and voltage settings, migration distances are converted to relative mobility ($R_f$):

$$R_f = \frac{d_{\text{sample}}}{d_{\text{total}}} = \frac{y_{\text{band}} - y_{\text{well}}}{y_{\text{front}} - y_{\text{well}}}$$

where:
- $y_{\text{band}}$ is the vertical migration coordinate of the band.
- $y_{\text{well}}$ is the origin coordinate at the loading well.
- $y_{\text{front}}$ is the migration position of the dye front or terminal gel edge.

### Semi-Logarithmic Regression (Ferguson Model)

The empirical relationship between molecular size ($M$) and relative mobility ($R_f$) in gel electrophoresis is described by the linear semi-log model across standard resolution ranges:

$$\log_{10}(M) = a \cdot R_f + b$$

Taking the anti-log gives the fragment size estimate:

$$M = 10^{a \cdot R_f + b}$$

where $a$ is the slope (slashing factor reflecting matrix gel density) and $b$ is the y-intercept.

### High-MW Non-Linearity and Non-Linear Models

For large biomolecules, matrix pore size limits sieving effectiveness, causing bands to migrate in a reptation regime where migration rate loses linear correlation with $\log_{10}(M)$. In these regions, polynomial semi-log regression (2nd or 3rd order) or local spline interpolation models provide higher accuracy:

$$\log_{10}(M) = c_2 \cdot R_f^2 + c_1 \cdot R_f + c_0$$

### Gel Smile Correction Physics

During electrophoresis, Joule heating generates thermal energy ($P = I^2 R$). Heat dissipation occurs predominantly through the lateral gel boundaries, creating a transverse temperature gradient where the gel center runs warmer than the edges. Because buffer viscosity decreases and electrophoretic mobility increases with temperature, bands in central lanes migrate faster than bands in lateral lanes, producing a curved front known as the "smile effect".

Dual-ladder calibration corrects for smile distortion by weighting migration reference coordinates based on horizontal lane position ($x$):

$$R_f^{\text{corrected}}(x, y) = (1 - w(x)) \cdot R_{f,\text{left}}(y) + w(x) \cdot R_{f,\text{right}}(y)$$

where $w(x) = \frac{x - x_{\text{left}}}{x_{\text{right}} - x_{\text{left}}}$ is the normalized horizontal position of the sample lane between the flanking ladders.

# Frequently Asked Questions

### 1. How do I estimate DNA band size from an agarose gel?
To estimate DNA band size, determine the relative migration distance ($R_f$) of known ladder bands and unknown sample bands. Plot $\log_{10}(\text{size in bp})$ against $R_f$ for the ladder bands to generate a standard curve linear equation $\log_{10}(\text{size}) = a \cdot R_f + b$. Calculate the $R_f$ of your sample band, substitute it into the standard curve equation, and compute $10^{(a \cdot R_f + b)}$ to obtain the estimated base pair size.

### 2. What is relative migration distance ($R_f$) in gel electrophoresis?
Relative migration distance ($R_f$), or relative mobility, is the ratio of the distance migrated by a specific DNA, RNA, or protein band relative to the total distance migrated by the dye front (or maximum gel migration length), measured from the loading well origin. Formula: $R_f = (y_{\text{band}} - y_{\text{well}}) / (y_{\text{front}} - y_{\text{well}})$.

### 3. Why is semi-log regression used for gel band molecular weight estimation?
Semi-log regression is used because the mobility of charged linear biomolecules through a sieving gel matrix is inversely proportional to the logarithm of their molecular mass or length in base pairs. Plotting $\log_{10}(\text{molecular size})$ against linear migration distance yields a straight line over the linear separation range of the gel.

### 4. How do I calculate a DNA standard curve for gel electrophoresis?
Measure the migration distance of each ladder band from the loading well, calculate $R_f$, and transform each known fragment size to $\log_{10}(\text{bp})$. Perform linear regression with $R_f$ as the independent variable ($x$) and $\log_{10}(\text{bp})$ as the dependent variable ($y$). The slope ($a$), intercept ($b$), and coefficient of determination ($R^2$) define the standard curve.

### 5. What causes gel smiling and how does dual-ladder correction fix it?
Gel smiling occurs when non-uniform heat dissipation across the gel causes central lanes to run warmer than outer lanes, causing central bands to migrate faster. Dual-ladder correction uses standard ladders loaded in both the leftmost and rightmost lanes. By calculating standard curves for both ladders and horizontally interpolating baseline mobility according to lane position, smile-induced sizing error is eliminated.

### 6. How do I determine protein molecular weight on SDS-PAGE?
On SDS-PAGE, sodium dodecyl sulfate (SDS) denatures proteins and confers a uniform negative charge-to-mass ratio. Protein bands migrate based solely on polypeptide chain length. Measure band migration relative to a pre-stained protein molecular weight ladder, plot $\log_{10}(\text{kDa})$ vs $R_f$, and solve for unknown sample band molecular weights in kilodaltons.

### 7. What is a good $R^2$ value for a gel electrophoresis standard curve?
A high-quality standard curve should achieve $R^2 \ge 0.98$ (ideally $R^2 \ge 0.99$). An $R^2$ below $0.95$ indicates potential measurement errors in band positions, gel overloading, distorted band morphology, or attempting to fit bands outside the linear sieving range of the gel concentration.

### 8. How does agarose gel concentration affect DNA band resolution range?
Higher agarose concentrations (e.g., 2.0% to 3.0%) create smaller matrix pores, resolving small DNA fragments (100 bp to 1,000 bp). Lower agarose concentrations (e.g., 0.7% to 1.0%) provide larger pores suitable for separating large DNA fragments (1,000 bp to 10,000+ bp).

### 9. What is the difference between a 100 bp ladder and a 1 kb ladder?
A 100 bp DNA ladder consists of fragments typically ranging from 100 bp to 1,000 bp or 1,500 bp in 100 bp increments, optimized for small PCR products. A 1 kb DNA ladder covers a broader range from 500 bp up to 10,000 bp (10 kb), suitable for restriction digests, genomic DNA fragments, and plasmid vectors.

### 10. Can Ladder Lens extrapolate sizes beyond the ladder markers?
While Ladder Lens can calculate mathematical extrapolation for bands migrating beyond the smallest or largest ladder bands, extrapolation is discouraged because gel migration loses linearity outside the calibrated range. Ladder Lens generates explicit warnings when sample migration falls outside ladder boundaries.

### 11. What is the formula $C_1 V_1 = C_2 V_2$ and how does it relate to gel loading?
$C_1 V_1 = C_2 V_2$ is the concentration/volume dilution formula used to prepare gel loading samples and running buffers (e.g., diluting 50X TAE or 10X TBE stock solutions to 1X working concentration, or preparing DNA samples with 6X loading dye).

### 12. How do I choose between linear and polynomial fit models?
Use semi-log linear regression for standard gels where sample bands fall within the central linear sieving range of the ladder. Use polynomial (2nd-order semi-log) fitting if your ladder covers extreme molecular weight ranges where high-MW compression or low-MW diffusion causes departure from linearity.

### 13. How does DNA conformation affect migration speed in agarose gels?
Uncut plasmid DNA exists in supercoiled, relaxed circular (nicked), and linear conformations. Supercoiled DNA migrates fastest due to its compact shape, followed by linear DNA, while relaxed circular DNA migrates slowest. Standard ladder calibration curves are strictly valid only for linear nucleic acids.

### 14. What image measurement units can I use with Ladder Lens?
Ladder Lens accepts any linear spatial measurement unit, including pixels, millimeters (mm), or centimeters (cm). Because $R_f$ is a dimensionless ratio of distances, the spatial unit cancels out, provided all band coordinates for a gel are measured using the same scale.

### 15. How do I report gel band size estimation methods in a scientific paper?
Report the gel percentage, buffer system, ladder manufacturer and catalogue number, model fit type (semi-log linear regression), $R^2$ goodness-of-fit value, and software tool used. Ladder Lens automatically outputs publication-ready methods text in its API and web response envelopes.

### 16. Can Ladder Lens be integrated into automated bioinformatics pipelines?
Yes. Ladder Lens provides a REST API and a Python client package (`pepkio-ladder-lens`) allowing automated band sizing to be integrated into high-throughput image processing pipelines, LIMS systems, and laboratory automation workflows.

# Web Application

The web version of Ladder Lens (https://www.pepkio.com/tools/ladder-lens) provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Researchers can use the web interface to upload gel image data, interactively mark band positions, select pre-loaded commercial ladder standards (e.g., NEB, Thermo Fisher, Bio-Rad), dynamically inspect standard curves, and export formatted reports.

- Web Application: https://www.pepkio.com/tools/ladder-lens

# Related Resources

- GitHub Repository: https://github.com/pepkio/pepkio-ladder-lens
- PyPI Package: https://pypi.org/project/pepkio-ladder-lens/
- Web Application: https://www.pepkio.com/tools/ladder-lens

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Scientific analysis capabilities include:
- RNA-seq analysis
- Single-cell RNA-seq analysis
- Spatial transcriptomics analysis
- Functional enrichment analysis
- Custom bioinformatics workflows

Website: https://www.pepkio.com/

# Citation

If you use Ladder Lens in your research or lab protocols, please cite:

```bibtex
@software{pepkio_ladder_lens,
  author = {Pepkio},
  title = {Ladder Lens: Gel Electrophoresis Band Size Estimator and Molecular Weight Calibration Tool},
  year = {2026},
  url = {https://www.pepkio.com/tools/ladder-lens}
}
```

# License

This project is licensed under the MIT License - see the `LICENSE` file for details.

# Keywords

ladder lens
pepkio ladder lens
gel electrophoresis band sizing
DNA molecular weight calculator
agarose gel band size estimator
SDS-PAGE protein mass calculator
relative migration distance calculator
Rf value gel electrophoresis
semi log regression gel electrophoresis
dual ladder gel smile correction
DNA ladder standard curve
gel band size calculation formula
base pair size calculator gel
molecular weight marker calibration
1 kb DNA ladder migration curve
100 bp DNA ladder standard curve
protein kilodalton calculator gel
gel smile effect compensation
electrophoretic mobility formula
ferguson plot gel electrophoresis
agarose gel fragment sizing
polyacrylamide gel sizing
band sizing software python
pcr amplicon size verification
restriction digest fragment sizing
crispr cas9 cleavage band quantification
ngs library fragment length estimation
rna integrity gel analysis
linear vs polynomial fit gel ladder
gel band pixel migration coordinate
R squared standard curve gel
gel band extrapolation warning
gel image band analysis tool
automated gel electrophoresis calculator
molecular weight determination software
gel lane smile correction algorithm
semi logarithmic band calibration
loading dye front Rf calculation
protein mass determination sds page
DNA fragment length curve fitting
bioinformatics gel analysis library
python gel electrophoresis client
pepkio scientific tools
molecular biology lab calculator
gel band migration ratio
agarose gel electrophoresis size analysis
linearized plasmid sizing gel
gel ladder interpolation python
biochemistry gel mass calculator
how to calculate DNA band size from gel
how to calculate Rf value gel electrophoresis
semi log standard curve formula DNA gel
how to fix gel smiling in size estimation
how to calculate protein molecular weight SDS PAGE
agarose gel concentration fragment size range
calculating base pairs from migration distance
gel band molecular weight estimation software
dual ladder horizontal interpolation gel
how to prepare standard curve for DNA ladder
what is a good R squared for gel standard curve
gel electrophoresis size estimation python script
automated DNA ladder band sizing API
estimating PCR product size on agarose gel
restriction fragment size estimation tool
protein ladder kilodalton estimation formula
difference between 100bp and 1kb ladder resolution
how gel temperature affects migration smile effect
calculating relative mobility in polyacrylamide gel
semi log linear regression base pair calculation
