# Package initializer: exposes main sequence utilities from core.py

from .core import (
    is_nucleic_acid,
    transcribe,
    reverse,
    complement,
    reverse_complement,
)

__all__ = [
    "is_nucleic_acid",
    "transcribe",
    "reverse",
    "complement",
    "reverse_complement",
]
