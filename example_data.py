# Small dataset and quick manual tests for the package

from main import run_dna_rna_tools, filter_fastq

# name -> (sequence, quality)
READS = {
    "dna":      ("ATGCAT", "IIIIII"),
    "rna":      ("AUGC",   "IIII"),
    "lowq":     ("GGGG",   "!!!!"),   # very low quality
    "short":    ("AT",     "II"),
    "mix_TU":   ("AUTG",   "IIII"),   # invalid: T and U mixed
    "mismatch": ("ATGC",   "III"),    # length mismatch
}


def run_asserts():
    # core tools
    assert run_dna_rna_tools("ATGC", proc_name="is_nucleic_acid") is True
    assert run_dna_rna_tools("AUTG", proc_name="is_nucleic_acid") is False
    assert run_dna_rna_tools("ATGC", proc_name="reverse") == "CGTA"
    assert run_dna_rna_tools("ATGC", proc_name="reverse_complement") == "GCAT"
    assert run_dna_rna_tools("ATGC", proc_name="transcribe") == "AUGC"

    # filter_fastq (defaults)
    kept = filter_fastq(READS)
    assert "mismatch" not in kept
    assert "mix_TU" not in kept
    assert "dna" in kept

    # typical bounds
    kept2 = filter_fastq(READS, gc_bounds=(40, 60), length_bounds=(4, 100), quality_threshold=30)
    assert set(kept2.keys()) <= set(READS.keys())

    # single-number bounds (treated as upper limits)
    kept3 = filter_fastq(READS, gc_bounds=70, length_bounds=6, quality_threshold=20)
    assert set(kept3.keys()) <= set(READS.keys())


if __name__ == "__main__":
    run_asserts()
    print("OK")