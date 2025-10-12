# Bioinformatics Tools
The project includes simple DNA/RNA utilities:
- check if a sequence is a valid nucleic acid;
- transcribe DNA -> RNA;
- get reverse, complement, and reverse–complement strands;
- filter FASTQ reads by GC content, length, and average quality;
- read FASTQ from a file and save filtered reads to the filtered/ folder;
- convert multiline FASTA records to one line per sequence (→ filtered/<name>);
- parse a BLAST text report and keep the first/top match for each input sequence,
  writing unique descriptions (sorted) to filtered/<name>.

## Project structure
```
│
├── modules/                          # package with sequence utilities
│   ├── __init__.py                   # package initializer: re-exports core functions
│   └── core.py                       # core DNA/RNA functions
│
├── example_data/                     # example inputs for HW5
│   ├── example_fastq.fastq
│   ├── example_multiline_fasta.fasta
│   └── example_blast_results.txt
│
├── filtered/                         # all outputs are written here
│   └── (generated files, e.g. output.fastq, oneline.fasta, blast_hits.txt)
│
├── fastq_utils.py                    # FASTQ reader + streaming filtering
├── bio_files.py                      # FASTA one-line + BLAST top-hit parser
├── main_new.py                           # entry point: runs FASTQ filtering
├── example_data.py                   # small dataset + self-test (from HW4)
└── README.md                         # project description and usage guide
```
## Install / Run
- Git clone and run:
  ```bash
  git clone <YOUR_REPO_URL>
  cd <YOUR_REPO_FOLDER>
  python --version  # Python 3.x
  ```

## Usage example
```python
from main_new import run_dna_rna_tools, filter_fastq

# DNA/RNA utilities
print(run_dna_rna_tools("ATGC", proc_name="reverse"))             # CGTA
print(run_dna_rna_tools("ATGC", proc_name="reverse_complement"))  # GCAT
print(run_dna_rna_tools("ATGC", proc_name="transcribe"))          # AUGC

# FASTQ filtering
reads = {
    "dna": ("ATGCAT", "IIIIII"),
    "rna": ("AUGC", "IIII"),
    "bad": ("AUTG", "IIII"),
    "lowq": ("GGGG", "!!!!"),
    "short": ("AT", "II"),
}
kept = filter_fastq(reads, gc_bounds=(0, 100), length_bounds=(3, 10), quality_threshold=30)
print(kept)
# → {'dna': ('ATGCAT', 'IIIIII'), 'rna': ('AUGC', 'IIII')}
```

## FASTQ filtering (from a file, streaming)

**Run the ready-made entry point:**
```bash
python main_new.py
# Done! Reads saved: <N>
# File written to: filtered/output.fastq
```

**Or call the function directly and change thresholds:**
```python
from fastq_utils import filter_fastq

filter_fastq(
    "example_data/example_fastq.fastq",
    "output.fastq",   # saved as filtered/output.fastq
    min_len=3,        # minimal read length
    min_qual=30       # minimal average PHRED33 quality
)
```

## FASTA — convert multiline sequences to one line
```python
from bio_files import convert_multiline_fasta_to_oneline

convert_multiline_fasta_to_oneline(
    "example_data/example_multiline_fasta.fasta",
    "oneline.fasta"   # -> filtered/oneline.fasta
)
```

## BLAST — keep the first/top match for each input sequence
```python
from bio_files import parse_blast_output

n = parse_blast_output(
    "example_data/example_blast_results.txt",
    "blast_hits.txt"  # -> filtered/blast_hits.txt
)
print("unique descriptions:", n)
```

## Notes
- The folder `modules/` is recognized as a Python package because it contains an `__init__.py` file.
- This file re-exports functions from `core.py`, allowing short imports like:
  ```python
  from modules import reverse_complement
  ```
- Create the output folder once:
    mkdir filtered.

## Compliance with assignment
- Uses only Python standard library (no external deps).
- Files are parsed manually, line by line (no biopython).
- FASTQ filtering is streaming (one read in memory).
- FASTA: multiline -> one-line per record.
- BLAST: text report parsed; first/top hit per Query collected.
- README is kept up to date with usage and arguments.