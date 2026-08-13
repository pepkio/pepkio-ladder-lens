# Pepkio Ladder Lens

Call the Pepkio ladder-lens REST API from Python to estimate DNA, RNA, or protein band sizes from gel electrophoresis migration distances using calibrated semi-log regression models.

# What It Does

In gel electrophoresis, estimating unknown sample band sizes (in bp, kb, or kDa) requires measuring migration distances against reference molecular weight markers. Manual interpolation from gel images is subjective, labor-intensive, and fails to correct for non-uniform electrophoretic mobility ("gel smiling") across lanes.

This package provides a Python client and CLI to submit band mobility measurements to the Pepkio Tools API. It calculates relative mobility ($R_f$), fits semi-log linear or 2nd-order polynomial calibration curves, performs dual-ladder gel smile correction, and returns estimated sample sizes alongside $R^2$ goodness-of-fit metrics and publication-ready methods text.

Programmatic runs require an active network connection and a Pepkio API key. Calculations are processed via the remote API and are not bundled for offline execution.

# Features

- Semi-log regression modeling: linear ($\log_{10}(\text{size})$ vs $R_f$) and 2nd-order log-polynomial fits
- Dual-ladder gel smile correction: interpolates across left and right reference lanes to compensate for thermal and edge distortion
- Relative mobility ($R_f$) calculation: converts band pixel coordinates ($y_{\text{well}}$, $y_{\text{front}}$, $y_{\text{band}}$) into normalized mobility values
- Goodness-of-fit diagnostics: reports $R^2$ coefficients and alerts on out-of-range band extrapolation
- Flexible unit support: nucleic acid fragment length (bp, kb) and protein molecular mass (kDa)
- Automated methods prose generator: outputs scientific methodology text for lab notebooks and research manuscripts
- Manifest and example inspection: `get_manifest()`, `list_examples()`, and `get_example_input()`
- Command-line interface: `pepkio-ladder-lens manifest` and `run`
- Environment configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-ladder-lens
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create an API key in your [Pepkio account settings](https://www.pepkio.com/account/api-keys).

# Quick Example

```python
from pepkio_ladder_lens import PepkioClient

with PepkioClient() as client:
    # Retrieve pre-configured input example from the API manifest
    inp = client.get_example_input("neb_1kb_single_ladder")
    result = client.run(inp)

    # Print regression quality and estimated band sizes
    print(f"Fit R²: {result.result['fit']['r_squared']}")
    for sample in result.result["samples"]:
        print(f"{sample['label']}: {sample['estimated_size_display']}")
```

CLI:

```bash
pepkio-ladder-lens run --example neb_1kb_single_ladder
```

Manifest inspection (`get_manifest()`, `list_examples()`) does not require an API key.

# Typical Use Cases

- PCR amplicon size verification against 100 bp or 1 kb DNA ladders
- Restriction fragment length determination following endonuclease digests
- SDS-PAGE target protein molecular weight estimation (kDa)
- Gel smile artifact compensation across multi-lane agarose or polyacrylamide gels
- Quality control and size validation for genomic library preparation
- Automated band sizing in LIMS, image processing, or notebook pipelines

# Scientific Background

Electrophoretic mobility of linear biomolecules in gel matrices scales logarithmically with molecular mass or sequence length. Relative mobility ($R_f$) is defined as:

$$R_f = \frac{y_{\text{band}} - y_{\text{well}}}{y_{\text{front}} - y_{\text{well}}}$$

The engine fits standard ladder bands to either a semi-log linear model ($\log_{10}(\text{size}) = m \cdot R_f + b$) or a 2nd-order polynomial ($\log_{10}(\text{size}) = a \cdot R_f^2 + b \cdot R_f + c$). When dual ladders are provided, $R_f$ curves are weighted across lane positions to correct for non-linear gel smile distortion caused by thermal or field gradients.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/ladder-lens

The web version provides interactive gel image lane and band picking, visual standard curve plots, dual-ladder gel smile visualization, shareable run links, and downloadable PDF/CSV bench reports.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-ladder-lens

Web Application: https://www.pepkio.com/tools/ladder-lens

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

gel electrophoresis, molecular weight calibration, DNA band sizing, protein molecular weight, agarose gel analysis, SDS-PAGE sizing, ladder lens, relative mobility Rf, semi-log regression, gel smile correction, DNA ladder calibration, RNA fragment size, restriction fragment length, PCR amplicon size, 1kb DNA ladder, 100bp ladder, kDa estimation, band size calculator, molecular weight marker, gel image analysis, R squared fit, dual ladder interpolation, pepkio-ladder-lens, bioinformatic gel tool, Python gel API, calculate DNA band size from migration distance, estimate protein molecular weight SDS-PAGE, semi log linear fit gel electrophoresis ladder, correct gel smiling artifact across lanes, relative mobility Rf calculation gel band, automated DNA fragment sizing Python, molecular weight standard curve regression, PCR product verification agarose gel, dual ladder interpolation gel smile correction, Pepkio ladder lens API Python client, standard curve log10 size vs Rf, band size estimation LIMS pipeline, gel band size calculator API, how to estimate band size from DNA ladder, convert pixel coordinates to relative mobility, SDS-PAGE protein kDa standard curve fit, DNA fragment size analysis from Python, agarose gel image band size estimation
