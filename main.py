"""Entry point with two utilities:
- run_dna_rna_tools(*seqs, proc_name)
- filter_fastq(seqs, gc_bounds, length_bounds, quality_threshold)
"""

from bioseq import (
    is_nucleic_acid,
    transcribe,
    reverse,
    complement,
    reverse_complement,
)


def run_dna_rna_tools(*seqs, proc_name):
    """Apply a selected DNA/RNA function (reverse, complement, etc.) to sequences."""
    proc_map = {
        "is_nucleic_acid": is_nucleic_acid,
        "transcribe": transcribe,
        "reverse": reverse,
        "complement": complement,
        "reverse_complement": reverse_complement,
    }
    if proc_name not in proc_map:
        raise ValueError(f"Unknown procedure: {proc_name}")

    fn = proc_map[proc_name]
    out = []

    for s in seqs:
        if proc_name not in ("reverse", "is_nucleic_acid") and not is_nucleic_acid(s):
            out.append(None)
        else:
            out.append(fn(s))

    return out[0] if len(out) == 1 else out


def filter_fastq(
    seqs,
    gc_bounds=(0, 100),
    length_bounds=(0, 2**32),
    quality_threshold=0.0,
):
    """Keep only those reads whose GC%, length and average quality fit the given limits."""

    def norm(b, low_default):
        if isinstance(b, tuple):
            lo, hi = b
        else:
            lo, hi = low_default, b
        return (lo, hi) if lo <= hi else (hi, lo)

    lo_gc, hi_gc = norm(gc_bounds, 0)
    lo_len, hi_len = norm(length_bounds, 0)

    kept = {}

    for name, pair in seqs.items():
        if not isinstance(pair, tuple) or len(pair) != 2:
            continue
        seq, qual = pair

        if not isinstance(seq, str) or not isinstance(qual, str):
            continue
        elif len(seq) != len(qual):
            continue
        elif not is_nucleic_acid(seq):
            continue
        elif len(seq) == 0:
            continue
        else:
            L = len(seq)
            gc = (sum(ch in "GgCc" for ch in seq) * 100.0) / L
            qmean = sum(ord(c) - 33 for c in qual) / L

            if (lo_len <= L <= hi_len) and (lo_gc <= gc <= hi_gc) and (qmean >= quality_threshold):
                kept[name] = (seq, qual)

    return kept
