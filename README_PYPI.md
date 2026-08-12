# Pepkio Instant Restriction Mapper

`pepkio-instant-restriction-mapper` is a Python client for scanning DNA sequences for restriction endonuclease cut sites, identifying single-cutter cloning vectors, and modeling fragment size distributions.

# What It Does

Restriction mapping is a foundational workflow in recombinant DNA technology, plasmid construction, and diagnostic cloning verification. Manual restriction site analysis is prone to errors due to degenerate IUPAC nucleotide codes, non-palindromic recognition sequences, overhang offsets, and circular plasmid topology origin wrapping.

This package provides a programmatic client for the Pepkio Tools REST API. It enables researchers to scan linear or circular DNA sequences against REBASE-curated restriction endonucleases, locate exact 5' and 3' strand cleavage positions, classify overhang chemistry, filter for single cutters, and compute fragment length distributions for single or multi-enzyme restriction digests.

# Features

- **REBASE-Curated Enzyme Engine**: Maps recognition sites for standard Type II, Type IIP, Type IIS, and Type IIT restriction endonucleases (e.g., EcoRI, BamHI, HindIII, BsaI, BsmBI, XhoI).
- **Topology-Aware Fragment Analysis**: Correctly calculates cleavage positions and fragment length distributions for circular plasmids (accounting for origin-spanning fragments) and linear DNA templates.
- **Cut Frequency & Single-Cutter Filtering**: Rapidly identifies unique single cutters for cloning vector linearization and MCS design.
- **Overhang & Geometry Classification**: Reports exact strand cleavage coordinates and overhang types (5' sticky, 3' sticky, or blunt end).
- **Multi-Enzyme Digest Simulation**: Computes expected restriction fragment size lists for single or double digestions.
- **Python Client & CLI**: Provides typed Pydantic models, synchronous and asynchronous execution, and CLI command execution (`pepkio-instant-restriction-mapper`).

# Installation

Install the package from PyPI using `pip`:

```bash
pip install pepkio-instant-restriction-mapper
```

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

# Quick Example

```python
from pepkio_instant_restriction_mapper import PepkioClient, RestrictionMapperInput

# Analyze a circular plasmid sequence for unique restriction cut sites
with PepkioClient() as client:
    request = RestrictionMapperInput(
        sequence="AGCTTGGCACTGGCCGTCTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCTGGTTTCCGGCACCAGAAGCGGTGCCGGAAAGCTGGCTGGAGTGCGATCTTCCTGAGGCCGATACTGTCGTCGTCCCCTCAAACTGGCAGATGCACGGTTACGATGCGCCCATCTACACCAACGTAACCTATCCCATTACGGTCAATCCGCCGTTTGTTCCCACGGAGAATCCGACGGGTTGTTACTCGCTCACATTTAATGTTGATGAAAGCTGGCTACAGGAAGGCCAGACGCGAATTATTTTTGATGGCGTTCCTATTGGTTAAA",
        sequence_name="pUC19_mini_region",
        topology="circular",
        cut_frequency=1,  # Unique single cutters
        hide_short_sites=True,
    )
    result = client.run(request)

    if result.result:
        sites = result.result.get("sites", [])
        print(f"Found {len(sites)} unique restriction sites:")
        for site in sites[:5]:
            print(f"- {site['enzyme']}: Cut Position {site['cut_positions']}, Pattern: {site['pattern']}")
```

You can also run analysis via the CLI:

```bash
pepkio-instant-restriction-mapper run \
  --sequence "GAATTCGCGGCCGCGGATCCGAATTC" \
  --topology linear \
  --cut-frequency 1
```

# Typical Use Cases

- **Plasmid Vector MCS Mapping**: Identify unique single-cutter restriction sites within vector multiple cloning sites for backbone linearization.
- **Diagnostic Digest Verification**: Predict fragment size distributions for single or double restriction digests to confirm recombinant clone insertion and orientation.
- **Golden Gate & Type IIS Assembly**: Screen constructs for non-palindromic Type IIS sites (e.g., BsaI, BsmBI, SapI) cutting outside their recognition motifs.
- **RFLP Variant Screening**: Pinpoint single nucleotide polymorphisms or indels that introduce or abolish restriction recognition motifs.
- **Synthetic Gene Quality Control**: Screen custom gene blocks for internal restriction sites before commercial synthesis ordering.

# Scientific Background

Type II restriction endonucleases recognize specific double-stranded DNA motifs (typically 4–8 bp) and catalyze site-specific phosphodiester bond cleavage.

For a DNA sequence with equal base frequencies ($25\%\text{ A}, \text{T}, \text{G}, \text{C}$), the probability $P$ of finding a non-degenerate recognition site of length $n$ is:

$$P = \left(\frac{1}{4}\right)^n$$

A 6-bp recognition motif (hexanucleotide cutter) occurs on average once every $4^6 = 4,096\text{ bp}$.

Topological context determines fragment output. For circular DNA cut at $N$ positions ($p_1 < p_2 < \dots < p_N$), exactly $N$ fragments are formed, with the origin-spanning fragment size computed as $S_N = (L - p_N) + p_1$ (where $L$ is total plasmid length). For linear DNA cut at $N$ positions, $N + 1$ fragments are generated.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/instant-restriction-mapper

The web application provides interactive restriction map visualization, a virtual agarose gel electrophoresis band simulator, customizable gel lane rendering, ELN protocol worksheets, and shareable permalink URLs.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-instant-restriction-mapper

Web Application: https://www.pepkio.com/tools/instant-restriction-mapper

Source code and issue tracking are maintained on [GitHub](https://github.com/pepkio/pepkio-instant-restriction-mapper).

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). The platform offers computational utilities for sequence analysis, molecular cloning workflows, and custom data processing.

# Keywords

* restriction mapping
* restriction enzyme finder
* restriction site analyzer
* plasmid restriction map
* DNA cleavage site finder
* restriction digest simulator
* virtual gel electrophoresis
* REBASE restriction enzyme database
* unique cutter finder
* single cutter restriction site
* isoschizomer finder
* neoschizomer finder
* restriction fragment size calculator
* double digest planner
* plasmid vector MCS mapper
* Type IIS restriction site
* EcoRI cut site mapper
* BamHI restriction site
* HindIII restriction mapping
* BsaI Golden Gate mapping
* BsmBI assembly planner
* linear vs circular DNA restriction
* 5 prime sticky overhang finder
* 3 prime sticky overhang finder
* blunt end restriction cleavage
* RFLP restriction site analysis
* synthetic gene restriction screening
* Python restriction mapper
* pepkio-instant-restriction-mapper
* molecular cloning restriction planner
* how to find unique restriction sites in plasmid vector
* calculate DNA restriction digest fragment lengths Python
* restriction enzyme cut frequency circular DNA calculator
* predict agarose gel band sizes from restriction digest
* screen synthetic gene for internal BsaI restriction sites
* identify 5 prime cohesive overhang restriction enzymes
* map multiple cloning site MCS restriction endonucleases
* restriction digest double cut fragment size calculator
* automated plasmid vector restriction mapping Python API
* REST API restriction enzyme recognition site scanner
