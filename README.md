# Pepkio Instant Restriction Mapper

Analyze restriction enzyme cut sites, generate restriction maps, simulate virtual digest fragments, and plan molecular cloning strategies in Python and via web interface.

# Overview

In molecular biology, genetic engineering, and recombinant DNA technology, restriction endonucleases (restriction enzymes) serve as essential molecular tools for precise DNA cleavage. Restriction mapping involves scanning a double-stranded DNA sequence (such as a plasmid vector, PCR product, synthetic gene, or viral genome) to locate specific recognition sequences, identify cleavage sites, and predict the exact molecular weights and lengths of resulting DNA fragments.

Accurate restriction mapping is critical for constructing recombinant plasmids, verifying gene insertion orientation, designing molecular cloning schemes (such as traditional restriction-ligation cloning, Gibson Assembly, and Golden Gate Assembly), preparing Restriction Fragment Length Polymorphism (RFLP) assays, and verifying plasmid constructs via diagnostic restriction digests.

Manual identification of restriction enzyme recognition sites is error-prone due to palindromic symmetry variations, degenerate nucleotide ambiguity codes (IUPAC bases), overlapping recognition motifs, and differences between circular plasmid topology and linear DNA fragments. Furthermore, manual fragment size calculation across plasmid origin coordinates (the 1 bp mark) frequently leads to incorrect fragment length predictions and mismatched agarose gel band patterns.

The **Pepkio Instant Restriction Mapper** provides a deterministic restriction mapping engine and fragment analysis platform. It scans linear or circular DNA sequences against REBASE-curated restriction endonucleases (Type II, Type IIP, Type IIS, and Type IIT), pinpoints exact 5' and 3' strand cleavage positions, classifies cleavage geometry (5' overhang, 3' overhang, or blunt end), filters by cut frequency (such as unique single cutters or rare cutters), identifies isoschizomers and neoschizomers, and simulates virtual agarose gel electrophoresis band patterns.

Researchers can access the hosted [Pepkio Instant Restriction Mapper](https://www.pepkio.com/tools/instant-restriction-mapper) web application for interactive restriction map visualization and gel simulation. A programmatic Python client (`pepkio-instant-restriction-mapper`) and command-line interface (CLI) are available for pipeline integration and automated batch processing.

Common search terms and alternative terminology for this tool include restriction map generator, restriction enzyme finder, plasmid restriction mapper, DNA restriction site analyzer, restriction digest simulator, virtual gel electrophoresis simulator, REBASE restriction enzyme database search, unique cutter finder, isoschizomer finder, restriction fragment size calculator, double digest planner, plasmid cleavage site mapper, and molecular cloning restriction analyzer.

# Features

- **REBASE-Curated Restriction Enzyme Database**: Scans DNA sequences against standard Type II, Type IIP, Type IIS, and Type IIT restriction endonucleases (including EcoRI, BamHI, HindIII, XhoI, NdeI, PstI, SpeI, XbaI, BsaI, BsmBI, and SapI).
- **Circular vs. Linear DNA Topology Awareness**: Accurately computes restriction cut positions and fragment length distributions for circular plasmids (wrapping across origin coordinates) and linear DNA templates (PCR amplicons, genomic fragments, or synthesized gene blocks).
- **Cut Frequency & Unique Cutter Filtering**: Filters enzymes by cleavage count (single cutters / unique restriction sites, double cutters, rare cutters, or all cut sites) to rapidly identify single-cut sites suitable for plasmid linearization and cloning vector construction.
- **Recognition Length & Isoschizomer Filtering**: Allows filtering by recognition motif length (e.g., 6-bp or 8-bp cutters, excluding short 4-bp frequent cutters) and option to toggle redundant isoschizomers for clean map representation.
- **Cleavage Geometry & Overhang Classification**: Reports precise 5' and 3' strand cut coordinates, identifying whether the enzyme yields a 5' cohesive overhang, 3' cohesive overhang, or blunt end.
- **Virtual Agarose Gel Electrophoresis Simulation**: Predicts DNA fragment mobility and resolves expected band patterns on virtual agarose gels based on logarithmic molecular weight separation.
- **Double Digest & Multi-Enzyme Fragment Analysis**: Calculates combined restriction fragment size lists resulting from single or multi-enzyme restriction digestions.
- **Python API & Command-Line Interface**: Asynchronous and synchronous Python client (`pepkio-instant-restriction-mapper`) and CLI executable for integration into computational biology pipelines (Nextflow, Snakemake, Jupyter).
- **Reproducible Permalinks**: Generates permanent calculation URLs to share exact restriction maps and digestion parameters across electronic lab notebooks (ELNs) and collaborative research teams.

# Common Use Cases

- **Plasmid Vector Mapping & Verification**: Scan circular vector backbones (such as pUC19, pET-28a(+), pCDNA3.1, or pBluescript) to generate restriction maps, identify unique cloning sites within the Multiple Cloning Site (MCS), and verify backbone integrity.
- **Recombinant DNA Cloning Strategy Design**: Select compatible restriction enzyme pairs for directional cloning, ensuring that selected enzymes do not cut within the target gene insert while generating compatible cohesive ends in the vector.
- **Diagnostic Restriction Digest Planning**: Predict expected fragment sizes and agarose gel band patterns for single or double restriction digests to confirm correct gene insertion and orientation following transformation.
- **Golden Gate & Type IIS Assembly Design**: Map non-palindromic Type IIS restriction sites (e.g., BsaI, BsmBI, SapI) that cut outside their recognition motifs, ensuring proper scarless assembly of multi-part genetic constructs.
- **Restriction Fragment Length Polymorphism (RFLP) Analysis**: Detect single nucleotide polymorphisms (SNPs) or indels that create or destroy specific restriction enzyme cut sites in genomic DNA or PCR amplicons.
- **Gene Synthesis Restriction Screening**: Screen custom synthetic DNA sequences for forbidden internal restriction sites before commercial synthesis ordering, ensuring compatibility with downstream cloning protocols.

# Why This Tool Exists

General sequence text editors, basic spreadsheet formulas (Excel, Google Sheets), and generic pattern matching utilities lack specialized molecular biology logic required for accurate restriction mapping. Standard regex tools fail to account for circular plasmid topology, where a restriction fragment spans the junction between the terminus and the 1-bp origin coordinate.

Manual restriction site searching is tedious and prone to errors when dealing with degenerate IUPAC nucleotide codes (e.g., $R = A/G, Y = C/T, N = A/C/G/T$), non-palindromic recognition sequences, or enzymes with cleavage sites located outside their recognition motifs (Type IIS enzymes). In addition, manual calculations often fail to identify isoschizomers (enzymes sharing identical recognition motifs) or neoschizomers (enzymes recognizing identical motifs but cutting at different positions), leading to unexpected overhang configurations during ligation.

Legacy desktop software applications often require local software installation, outdated runtime dependencies, or commercial license fees. Pepkio Instant Restriction Mapper provides a zero-installation web interface and programmatic API that delivers restriction map generation, virtual gel visualization, and reproducible data sharing.

# Installation

Install the Python client package from PyPI using `pip`:

```bash
pip install pepkio-instant-restriction-mapper
```

Or using `uv`:

```bash
uv add pepkio-instant-restriction-mapper
```

The official package distribution is indexed on [PyPI](https://pypi.org/project/pepkio-instant-restriction-mapper/).

# Quick Start

### Python API Usage

Set your API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Execute restriction mapping analysis in Python using `PepkioClient`:

```python
from pepkio_instant_restriction_mapper import PepkioClient, RestrictionMapperInput

# Initialize client
with PepkioClient() as client:
    # 1. Analyze circular plasmid sequence for unique restriction cutters
    mapper_input = RestrictionMapperInput(
        sequence="AGCTTGGCACTGGCCGTCTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCTGGTTTCCGGCACCAGAAGCGGTGCCGGAAAGCTGGCTGGAGTGCGATCTTCCTGAGGCCGATACTGTCGTCGTCCCCTCAAACTGGCAGATGCACGGTTACGATGCGCCCATCTACACCAACGTAACCTATCCCATTACGGTCAATCCGCCGTTTGTTCCCACGGAGAATCCGACGGGTTGTTACTCGCTCACATTTAATGTTGATGAAAGCTGGCTACAGGAAGGCCAGACGCGAATTATTTTTGATGGCGTTCCTATTGGTTAAA",
        sequence_name="pUC19_mini_region",
        topology="circular",
        cut_frequency=1,  # Single cutters only
        hide_short_sites=True,
        show_isoschizomers=False
    )
    
    result = client.run(mapper_input)
    
    print("Run Status:", result.status)
    print("Permalink:", result.permalink)
    
    # Access map results
    if result.result:
        sites = result.result.get("sites", [])
        print(f"Found {len(sites)} unique restriction sites:")
        for site in sites:
            print(f"- {site['enzyme']}: Cut Position {site['position']}, Recognition: {site['pattern']}")
```

### Command-Line Interface (CLI) Usage

Run restriction map analysis directly from the command line:

```bash
# Analyze a linear DNA sequence for single cutters
pepkio-instant-restriction-mapper run \
  --sequence "GAATTCGCGGCCGCGGATCCGAATTC" \
  --topology linear \
  --cut-frequency 1

# Fetch available manifest and examples
pepkio-instant-restriction-mapper manifest --examples
```

# Example Output

Below is a representative JSON response object returned by the restriction mapping API:

```json
{
  "run_id": "run_rm_9847102f",
  "status": "completed",
  "result": {
    "sequence_info": {
      "name": "pUC19_mini_region",
      "length_bp": 450,
      "topology": "circular",
      "gc_content_percent": 52.44
    },
    "summary": {
      "total_enzymes_analyzed": 245,
      "enzymes_with_cuts": 12,
      "unique_cutters_count": 5,
      "double_cutters_count": 3
    },
    "sites": [
      {
        "enzyme": "EcoRI",
        "pattern": "G^AATTC",
        "recognition_length": 6,
        "cut_positions": [1],
        "cut_count": 1,
        "overhang_type": "5_prime_sticky",
        "overhang_sequence": "AATT",
        "isoschizomers": ["FunHMII"]
      },
      {
        "enzyme": "BamHI",
        "pattern": "G^GATCC",
        "recognition_length": 6,
        "cut_positions": [18],
        "cut_count": 1,
        "overhang_type": "5_prime_sticky",
        "overhang_sequence": "GATC",
        "isoschizomers": ["BstI"]
      },
      {
        "enzyme": "HindIII",
        "pattern": "A^AGCTT",
        "recognition_length": 6,
        "cut_positions": [142],
        "cut_count": 1,
        "overhang_type": "5_prime_sticky",
        "overhang_sequence": "AGCT",
        "isoschizomers": []
      }
    ],
    "digest_fragments": {
      "selected_enzymes": ["EcoRI", "HindIII"],
      "fragment_count": 2,
      "fragment_sizes_bp": [141, 309]
    }
  },
  "permalink": "https://tools.pepkio.com/runs/run_rm_9847102f",
  "duration_ms": 18
}
```

# Scientific Background

### Restriction Endonucleases & Recognition Mechanisms

Restriction endonucleases are bacterial enzymes that recognize specific double-stranded DNA sequences and catalyze the cleavage of phosphodiester bonds on both strands. In nature, restriction-modification (R-M) systems protect bacteria against invading bacteriophage DNA by cleaving unmethylated viral genomes while host genomic DNA is protected by site-specific DNA methyltransferases.

Type II restriction enzymes are the primary class used in recombinant DNA technology. They typically recognize short palindromic sequences (4 to 8 base pairs in length) and cleave within or adjacent to their recognition motifs without requiring ATP hydrolysis.

### Expected Restriction Frequency & Base Composition

For a random DNA sequence with balanced base composition ($25\% \text{ A}, 25\% \text{ T}, 25\% \text{ G}, 25\% \text{ C}$), the probability $P$ of finding a specific non-degenerate restriction motif of length $n$ base pairs at any given position is:

\[
P = \left(\frac{1}{4}\right)^n
\]

Thus, the expected average distance $E(L)$ between cut sites for a 4-bp, 6-bp, or 8-bp cutter is:

- **4-bp cutter** (e.g., TaqI, MboI): \( E(L) = 4^4 = 256 \text{ bp} \)
- **6-bp cutter** (e.g., EcoRI, BamHI): \( E(L) = 4^6 = 4,096 \text{ bp} \)
- **8-bp cutter** (e.g., NotI, PacI): \( E(L) = 4^8 = 65,536 \text{ bp} \)

When template DNA exhibits GC-bias ($f_G + f_C = f_{GC}$), the site probability $P(s)$ for a recognition motif $s$ containing $N_{GC}$ GC pairs and $N_{AT}$ AT pairs is adjusted:

\[
P(s) = \left(\frac{f_{GC}}{2}\right)^{N_{GC}} \times \left(\frac{1 - f_{GC}}{2}\right)^{N_{AT}}
\]

### Topology & Restriction Fragment Calculation Mathematics

The mathematical relationship between cut site coordinates and resulting restriction fragment sizes depends on template topology (circular vs. linear).

#### Circular Topology (Plasmids & Circular DNA)
For a circular plasmid of total length $L$ bp cut at $N$ unique positions sorted in ascending order $p_1 < p_2 < \dots < p_N$:

- Total number of resulting DNA fragments = $N$
- Internal fragment lengths for $i = 1, 2, \dots, N-1$:
  \[
  S_i = p_{i+1} - p_i
  \]
- Origin-wrapping fragment length $S_N$:
  \[
  S_N = (L - p_N) + p_1
  \]

#### Linear Topology (PCR Amplicons & Linearized DNA)
For a linear DNA molecule of total length $L$ bp cut at $N$ positions $p_1 < p_2 < \dots < p_N$:

- Total number of resulting DNA fragments = $N + 1$
- 5'-terminal fragment length:
  \[
  S_1 = p_1
  \]
- Internal fragment lengths for $i = 2, 3, \dots, N$:
  \[
  S_i = p_i - p_{i-1}
  \]
- 3'-terminal fragment length:
  \[
  S_{N+1} = L - p_N
  \]

### Isoschizomers, Neoschizomers, and Isocaudomers

- **Isoschizomers**: Restriction enzymes isolated from different bacterial species that recognize the identical DNA sequence and cleave at the exact same position (e.g., SphI and BbuI both recognize `GCATG^C`).
- **Neoschizomers**: Restriction enzymes that recognize the identical DNA sequence but cleave at different positions within the motif, producing different overhang geometries (e.g., SmaI recognizes `CCC^GGG` producing blunt ends, whereas XmaI recognizes `C^CCGGG` producing 5' cohesive ends).
- **Isocaudomers**: Restriction enzymes that recognize different sequences but generate identical cohesive overhangs, allowing incompatible restriction sites to be ligated together (e.g., BamHI `G^GATCC` and XhoI/SalI/MboI derivatives).

### DNA Methylation Sensitivity

Bacterial host strains frequently express DNA methyltransferases (such as Dam methylase, Dcm methylase, or CpG methylases in mammalian systems) that modify specific cytosine or adenine residues:

- **Dam Methylation**: Methylates adenine in `GAmTC` sequences. Enzymes whose recognition sites overlap Dam methylation (e.g., ClaI, MboI, XbaI under specific context) can be blocked from cutting.
- **Dcm Methylation**: Methylates internal cytosine in `CCWGG` sequences ($W = A \text{ or } T$). Enzymes such as AvaII or EcoRII may be inhibited when plasmid DNA is isolated from $dcm^+$ E. coli strains (e.g., DH5$\alpha$, TOP10).
- **CpG Methylation**: Methylates cytosines in `CG` dinucleotides in eukaryotic DNA, blocking enzymes such as NotI, PstI, and XhoI.

### Virtual Agarose Gel Mobility Physics

During agarose gel electrophoresis under constant electric field strength, charged DNA fragments migrate toward the anode (+). The electrophoretic mobility $\mu$ of double-stranded DNA is inversely proportional to the logarithm of its molecular weight (or base pair length $L$):

\[
d = a - b \cdot \log_{10}(L)
\]

where $d$ is migration distance, and $a$ and $b$ are gel-specific constants determined by agarose concentration ($0.7\% - 2.0\%$), voltage gradient, and buffer ionic strength (TAE or TBE). Virtual gel simulations apply this logarithmic migration model to render realistic band patterns alongside standard DNA ladders (e.g., 1 kb DNA ladder, 100 bp ladder).

# Frequently Asked Questions

### What is a restriction map?
A restriction map is a structural map of a DNA molecule (plasmid, PCR product, or chromosome) that indicates the precise linear or circular positions of restriction enzyme recognition sites and cut locations.

### How does a restriction enzyme identify cut sites?
Restriction enzymes scan double-stranded DNA via 3D diffusion and 1D sliding along the phosphodiester backbone until encountering their specific recognition motif, where conformational binding induces phosphodiester bond hydrolysis.

### What is the difference between circular and linear DNA restriction digestion?
In circular DNA (plasmids), $N$ restriction cut sites yield exactly $N$ DNA fragments because the circular molecule opens at each cut. In linear DNA, $N$ restriction cut sites yield $N + 1$ DNA fragments.

### How do I calculate restriction fragment sizes for a double digest?
To calculate double digest fragment sizes, combine and sort all cut coordinates from both enzymes. Then compute adjacent coordinate differences (accounting for circular origin wrapping if the template is a plasmid).

### What are isoschizomers and neoschizomers?
Isoschizomers are different enzymes that recognize the same sequence and cut at the exact same position. Neoschizomers recognize the same sequence but cut at different positions, generating different overhang types.

### What is the difference between sticky ends and blunt ends?
Sticky (cohesive) ends have single-stranded 5' or 3' overhangs that facilitate complementary base-pairing during ligation. Blunt ends have fully paired double-stranded termini with no single-stranded overhangs.

### How does Dam and Dcm methylation affect restriction digestion?
Dam and Dcm methyltransferases add methyl groups to specific adenine (`GAmTC`) or cytosine (`CCWGG`) bases in E. coli. If a restriction site overlaps a methylated base, enzyme cleavage may be partially or completely inhibited.

### What is star activity in restriction enzyme digests?
Star activity is the relaxation of cleavage specificity under non-optimal reaction conditions (such as high glycerol concentrations, excess enzyme, wrong buffer pH, or low ionic strength), leading to cleavage at non-canonical sequences.

### How do I choose restriction enzymes for directional cloning?
Select two different restriction enzymes present in the vector Multiple Cloning Site (MCS) that do not cut within the target gene insert, ensure they yield non-compatible cohesive overhangs, and verify buffer compatibility for double digestion.

### How does virtual agarose gel electrophoresis simulation work?
Virtual agarose gel simulation calculates expected fragment lengths from restriction cut coordinates and models their migration distances using an inverse logarithmic relationship with fragment length ($d \propto -\log_{10} L$).

### What is the expected frequency of a 6-bp restriction cutter?
In a random sequence with equal base proportions ($50\% \text{ GC}$), a 6-bp cutter occurs once every $4^6 = 4,096 \text{ bp}$ on average.

### Why are unique cutters important in plasmid cloning?
Unique cutters cleave a plasmid vector at exactly one position, linearizing the plasmid without removing essential backbone elements or cutting the vector into multiple disassociated fragments.

### How do I calculate enzyme volumes for a restriction digest reaction ($C_1 V_1 = C_2 V_2$)?
Use the dilution formula $C_1 V_1 = C_2 V_2$ to calculate required volumes of $10\times$ restriction buffer, DNA template, enzyme units (typically 5–10 units per $\mu\text{g}$ DNA), and nuclease-free water to achieve desired final concentrations.

### What is the difference between Type II and Type IIS restriction enzymes?
Type II restriction enzymes recognize palindromic sequences and cut inside the recognition site. Type IIS restriction enzymes recognize asymmetric sequences and cleave DNA at a specified distance outside the recognition motif.

### How does Instant Restriction Mapper handle IUPAC degenerate nucleotide codes?
Instant Restriction Mapper expands degenerate IUPAC ambiguity codes (e.g., $R, Y, S, W, K, M, B, D, H, V, N$) into their corresponding nucleotide sets to accurately identify restriction sites containing ambiguous bases.

### How do circular plasmid coordinates handle fragments crossing the 1-bp origin?
For circular plasmids, if a restriction fragment spans across the origin, its length is calculated as $(L - p_{\text{last}}) + p_1$, where $L$ is total plasmid length, $p_{\text{last}}$ is the final cut coordinate, and $p_1$ is the first cut coordinate.

# Web Application

The hosted version of the tool is accessible at:

Web Application:
https://www.pepkio.com/tools/instant-restriction-mapper

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools. It allows researchers to upload FASTA or GenBank sequence files, interactively filter enzyme lists by cut frequency, toggle virtual agarose gel electrophoresis simulations, and export publication-ready restriction maps.

# Related Resources

GitHub Repository:
https://github.com/pepkio/pepkio-instant-restriction-mapper

PyPI Package:
https://pypi.org/project/pepkio-instant-restriction-mapper/

Web Application:
https://www.pepkio.com/tools/instant-restriction-mapper

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Pepkio provides computational workflows and specialized data analysis services across several domain areas, including:

- RNA-seq analysis
- Single-cell RNA-seq analysis
- Spatial transcriptomics analysis
- Functional enrichment analysis
- Custom bioinformatics workflows

Website:
https://www.pepkio.com/

# Citation

If you use Pepkio Instant Restriction Mapper in your research, software pipelines, or academic publications, please cite the tool as follows:

### Plain Text
Pepkio Instant Restriction Mapper. Pepkio Bioinformatics Tools. Available at: https://www.pepkio.com/tools/instant-restriction-mapper.

### BibTeX
```bibtex
@misc{pepkio_instant_restriction_mapper,
  title = {Pepkio Instant Restriction Mapper: Interactive and Programmatic Restriction Enzyme Mapping},
  author = {{Pepkio}},
  year = {2026},
  howpublished = {\url{https://github.com/pepkio/pepkio-instant-restriction-mapper}},
  note = {Software available from PyPI and GitHub}
}
```

# License

This project is licensed under the MIT License. See the `LICENSE` file for details.

# Keywords

pepkio-instant-restriction-mapper, instant restriction mapper, restriction map generator, restriction enzyme finder, plasmid restriction mapper, DNA restriction site analyzer, restriction digest simulator, virtual gel electrophoresis simulator, REBASE restriction enzyme search, unique cutter finder, isoschizomer finder, restriction fragment size calculator, double digest planner, plasmid cleavage site mapper, molecular cloning restriction analyzer, EcoRI cut site finder, BamHI restriction map, HindIII cleavage site, Type II restriction enzyme analyzer, Type IIS restriction enzyme mapper, Golden Gate assembly restriction planner, Gibson assembly restriction checker, 5 prime sticky end calculator, 3 prime sticky end calculator, blunt end restriction enzyme finder, Dam methylation restriction sensitivity, Dcm methylation restriction sensitivity, CpG methylation restriction blocking, circular DNA fragment size calculator, linear DNA digest simulator, restriction fragment length polymorphism RFLP analyzer, plasmid vector multiple cloning site mapper, pUC19 restriction map, pET28a restriction map, pCDNA31 restriction map, single cutter plasmid finder, rare cutter restriction enzyme, restriction endonuclease cleavage calculator, degenerate IUPAC restriction site search, restriction digest band pattern generator, agarose gel band mobility simulator, DNA restriction mapping Python library, restriction enzyme API client, bioinformatics restriction enzyme toolkit

instant restriction mapper online calculator, how to generate a restriction map for plasmid DNA, calculate DNA fragment sizes after double restriction digest, find unique restriction cut sites in plasmid vector, simulate agarose gel electrophoresis band patterns online, restriction enzyme recognition site finder for FASTA sequence, plasmid circular topology restriction fragment calculation formula, difference between circular and linear DNA restriction digestion fragments, how Dam and Dcm methylation blocks restriction enzyme cleavage, Type IIS restriction enzyme mapping for Golden Gate cloning, how to choose compatible restriction enzymes for directional cloning, find isoschizomers and neoschizomers for EcoRI and BamHI, calculate expected restriction site frequency in GC rich DNA, Python REST API client for REBASE restriction enzyme search, interactive restriction mapping tool for molecular biology labs
