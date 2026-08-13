# Pepkio Ladder Lens

Python client for the Pepkio Ladder Lens API: gel electrophoresis band size estimator for DNA/RNA agarose and protein SDS-PAGE gels.

## Features

- Semi-log regression calibration (log10 MW vs migration Rf)
- Supports semi-log linear and 2nd-order log-polynomial fit models
- Dual-ladder smile correction across gel lanes
- R² quality feedback and exportable methods text
- Manifest and named examples: `get_manifest`, `list_examples`, `get_example_input`
- CLI support: `pepkio-ladder-lens manifest` and `run`

## Installation

```bash
pip install pepkio-ladder-lens
```

Set your API key before running requests:

```bash
export PEPKIO_API_KEY="your-key"
```

## Python Usage

```python
from pepkio_ladder_lens import PepkioClient

with PepkioClient() as client:
    # Run named example from manifest
    inp = client.get_example_input("neb_1kb_single_ladder")
    result = client.run(inp)

    print(f"Fit R²: {result.result['fit']['r_squared']}")
    for s in result.result['samples']:
        print(f"{s['label']}: {s['estimated_size_display']}")
```

## CLI Usage

```bash
pepkio-ladder-lens manifest
pepkio-ladder-lens run --example neb_1kb_single_ladder
```
