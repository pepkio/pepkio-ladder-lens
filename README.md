# pepkio-ladder-lens

Python client for the [Pepkio Ladder Lens](https://www.pepkio.com/tools/ladder-lens) tool (gel electrophoresis band size estimator with semi-log regression, dual-ladder smile correction, and R² feedback).

## Installation

```bash
pip install pepkio-ladder-lens
```

## Quick Start

```python
from pepkio_ladder_lens import PepkioClient

client = PepkioClient(api_key="your-api-key")

# Fetch tool manifest
manifest = client.get_manifest()
print(manifest["title"])

# Run with an example
inp = client.get_example_input("neb_1kb_single_ladder")
result = client.run(inp)

print("Status:", result.status)
print("Fit R²:", result.result["fit"]["r_squared"])
for sample in result.result["samples"]:
    print(f"{sample['label']}: {sample['estimated_size_display']}")
```

## CLI Usage

```bash
export PEPKIO_API_KEY="your-api-key"

# View manifest
pepkio-ladder-lens manifest

# Run example
pepkio-ladder-lens run --example neb_1kb_single_ladder
```

## License

MIT
