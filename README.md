# HW4: Bioinformatics Tools

The project includes simple DNA/RNA utilities:
- check if a sequence is a valid nucleic acid;
- transcribe DNA → RNA;
- get reverse, complement, and reverse–complement strands;
- filter FASTQ reads by GC content, length, and average quality.

## Project structure
```
│
├── bioseq/                     # package with sequence utilities
│   ├── __init__.py             # package initializer: re-exports core functions
│   └── core.py                 # core DNA/RNA functions
│
├── main.py                     # entry point: run_dna_rna_tools() and filter_fastq()
├── example_data.py             # small dataset + self-test
└── README.md                   # project description and usage guide
```

## Usage example
```python
from main import run_dna_rna_tools, filter_fastq

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

## Notes
- The folder `bioseq/` is recognized as a Python package because it contains an `__init__.py` file.
- This file re-exports functions from `core.py`, allowing short imports like:
  ```python
  from bioseq import reverse_complement
  ```