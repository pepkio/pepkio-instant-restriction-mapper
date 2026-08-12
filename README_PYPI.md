# Pepkio Instant Restriction Mapper

`pepkio-instant-restriction-mapper` is a Python client and REST API wrapper for identifying restriction enzyme cleavage sites, screening single-cut cloning vectors, and predicting restriction fragment size distributions in circular and linear DNA sequences.

# What It Does

Restriction mapping is essential for plasmid vector design, recombinant DNA cloning, and diagnostic digest verification. Searching DNA sequences manually for restriction sites is prone to errors caused by degenerate IUPAC base codes, non-palindromic recognition motifs, 5'/3' overhang offsets, and circular topology origin wrapping.

This package connects Python scripts, Jupyter notebooks, and automated workflow pipelines to the Pepkio Tools REST API. It scans linear or circular DNA templates against REBASE-curated restriction endonucleases, identifies exact strand cut positions, classifies cleavage geometry (5' sticky, 3' sticky, or blunt end), filters unique cutters, and computes fragment size distributions for single or multi-enzyme digests.

Programmatic runs require a network connection and a Pepkio API key. Manifest and example queries do not require authentication.

# Features

- **REBASE-Curated Enzyme Database**: Scans sequences against standard Type II, Type IIP, Type IIS, and Type IIT restriction endonucleases (e.g., EcoRI, BamHI, HindIII, BsaI, BsmBI, XhoI).
- **Topology-Aware Fragment Calculation**: Accurately computes cut positions and fragment length distributions for circular plasmids (spanning the 1-bp origin) and linear DNA templates.
- **Cut Frequency & Unique Cutter Filtering**: Rapidly isolates single cutters (unique restriction sites) for vector linearization and cloning vector selection.
- **Overhang & Geometry Classification**: Reports 5' cohesive overhangs, 3' cohesive overhangs, and blunt-end cut sites with exact strand cleavage coordinates.
- **Multi-Enzyme Virtual Digest**: Computes predicted restriction fragment lengths resulting from single or double enzyme digestions.
- **Python Client & CLI**: Includes typed Pydantic models, synchronous and asynchronous client methods, and command-line execution (`pepkio-instant-restriction-mapper`).

# Installation

Install the package via `pip`:

```bash
pip install pepkio-instant-restriction-mapper
```

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

Keys can be generated in your [Pepkio API Settings](https://www.pepkio.com/account/api-keys).

# Quick Example

### Python API

```python
from pepkio_instant_restriction_mapper import PepkioClient, RestrictionMapperInput

# Analyze a circular plasmid sequence for unique restriction cutters
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
        print(f"Found {len(sites)} unique restriction cut sites.")
        for site in sites[:5]:
            print(f"- {site['enzyme']}: Cut position {site['cut_positions']}, Pattern: {site['pattern']}")
```

### CLI Command

```bash
pepkio-instant-restriction-mapper run \
  --sequence "GAATTCGCGGCCGCGGATCCGAATTC" \
  --topology linear \
  --cut-frequency 1
```

# Typical Use Cases

- **Plasmid Vector MCS Mapping**: Identify unique single-cutter restriction sites within multiple cloning sites (MCS) for vector linearization.
- **Diagnostic Restriction Digest Design**: Predict expected fragment size distributions to confirm correct recombinant clone insertion and orientation via agarose gel electrophoresis.
- **Golden Gate & Type IIS Assembly**: Locate non-palindromic Type IIS cleavage sites (BsaI, BsmBI, SapI) cutting outside their recognition sequences for scarless assembly.
- **Restriction Fragment Length Polymorphism (RFLP)**: Detect single-nucleotide polymorphisms or indels that introduce or abolish restriction recognition motifs.
- **Gene Synthesis Screening**: Screen synthetic gene constructs for unwanted internal restriction sites prior to commercial gene synthesis ordering.

# Scientific Background

Type II restriction endonucleases catalyze site-specific double-stranded DNA phosphodiester bond cleavage within or near palindromic recognition motifs.

For a random DNA sequence with equal base frequencies ($25\%\text{ A}, \text{T}, \text{G}, \text{C}$), the occurrence probability $P$ of a non-degenerate $n$-base restriction site is:

$$P = \left(\frac{1}{4}\right)^n$$

A hexanucleotide ($n = 6$) recognition motif occurs on average once every $4^6 = 4,096\text{ bp}$.

Topological context dictates fragment yield: a circular DNA molecule cleaved at $N$ restriction sites generates $N$ fragments, whereas a linear DNA molecule cleaved at $N$ sites produces $N + 1$ fragments. In circular plasmids, fragment calculation must correctly account for cleavage events spanning the origin (1-bp junction).

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/instant-restriction-mapper

The web application provides interactive restriction map diagrams, a virtual agarose gel electrophoresis band simulator, customizable gel lane comparison, ELN-ready protocol summaries, and permanent shareable result URLs.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-instant-restriction-mapper

Web Application: https://www.pepkio.com/tools/instant-restriction-mapper

Source code and issue tracking are maintained on [GitHub](https://github.com/pepkio/pepkio-instant-restriction-mapper).

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

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
