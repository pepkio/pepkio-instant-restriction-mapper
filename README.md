# pepkio-instant-restriction-mapper

Python client for the [Pepkio Instant Restriction Mapper](https://www.pepkio.com/tools/instant-restriction-mapper) REST API.

Find restriction enzyme recognition sites, methylation warnings, compatible overhangs, and fragment size distributions programmatically.

## Installation

```bash
pip install pepkio-instant-restriction-mapper
```

## Quick Start

```python
from pepkio_instant_restriction_mapper import PepkioClient

client = PepkioClient(api_key="your_api_key")

# Fetch manifest and examples
manifest = client.get_manifest()
print(manifest["title"])

# Run restriction mapping
result = client.run(
    {
        "sequence": "AAAAAAAAAAGAATTCAAAAAAAAAA",
        "topology": "linear",
        "cut_frequency": 1,
    }
)

print(result.status)
print(result.result)
```

## CLI Usage

```bash
# Print tool manifest
pepkio-instant-restriction-mapper manifest

# Run using a manifest example
pepkio-instant-restriction-mapper run --example eco_single_site

# Run with custom JSON input
pepkio-instant-restriction-mapper run --input-json '{"sequence": "ATGCGATCGAAGAATTC", "topology": "circular"}'
```

## License

MIT
