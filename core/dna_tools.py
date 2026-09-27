"""DNA sequence tools."""


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    sequence = sequence.upper().strip()
    result = []
    for base in reversed(sequence):
        if base not in complement:
            raise ValueError(f"Invalid base: {base}")
        result.append(complement[base])
    return "".join(result)


def gc_content(sequence: str) -> float:
    """Return GC content as a percentage."""
    sequence = sequence.upper().strip()
    if not sequence:
        return 0.0
    gc = sum(1 for base in sequence if base in ("G", "C"))
    return (gc / len(sequence)) * 100


def transcribe(sequence: str) -> str:
    """DNA -> RNA (T becomes U)."""
    return sequence.upper().strip().replace("T", "U")


def count_bases(sequence: str) -> dict:
    """Count each base in the sequence."""
    sequence = sequence.upper().strip()
    counts = {"A": 0, "T": 0, "G": 0, "C": 0}
    for base in sequence:
        if base in counts:
            counts[base] += 1
    return counts