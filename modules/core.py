"""Core utilities for DNA/RNA sequences.

Functions:
- is_nucleic_acid(seq)
- transcribe(seq)
- reverse(seq)
- complement(seq)
- reverse_complement(seq)
"""

from typing import Dict

_DNA_COMP: Dict[str, str] = {
    "A": "T", "T": "A", "G": "C", "C": "G",
    "a": "t", "t": "a", "g": "c", "c": "g",
}
_RNA_COMP: Dict[str, str] = {
    "A": "U", "U": "A", "G": "C", "C": "G",
    "a": "u", "u": "a", "g": "c", "c": "g",
}
_VALID = set("ATUGCatugc")


def is_nucleic_acid(seq: str) -> bool:
    """Return True iff `seq` consists only of A/T/U/G/C (any case) and does not mix T with U."""
    if not seq:
        return False
    has_t = False
    has_u = False
    for ch in seq:
        if ch not in _VALID:
            return False
        if ch in "Tt":
            has_t = True
        elif ch in "Uu":
            has_u = True
    return not (has_t and has_u)


def transcribe(seq: str) -> str:
    """DNA → RNA transcription (T/t → U/u). Raises ValueError if input looks like RNA."""
    if any(ch in ("U", "u") for ch in seq):
        raise ValueError("Input appears to be RNA (contains U). Transcription DNA→RNA not applicable.")
    res_chars = []
    for ch in seq:
        if ch == "T":
            res_chars.append("U")
        elif ch == "t":
            res_chars.append("u")
        else:
            res_chars.append(ch)
    return "".join(res_chars)


def reverse(seq: str) -> str:
    """Return reversed sequence."""
    return seq[::-1]


def complement(seq: str) -> str:
    """Return complement strand; preserves case. Auto-detects DNA vs RNA by presence of U/u."""
    table = _RNA_COMP if any(ch in ("U", "u") for ch in seq) else _DNA_COMP
    return "".join(table[n] for n in seq)


def reverse_complement(seq: str) -> str:
    """Return reverse complement."""
    return complement(reverse(seq))
