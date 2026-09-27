"""Genetic code and probability calculators."""

# Codon table: RNA codon -> amino acid (single-letter)
CODON_TABLE = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

AA_NAMES = {
    "A": "Alanine", "R": "Arginine", "N": "Asparagine", "D": "Aspartic acid",
    "C": "Cysteine", "Q": "Glutamine", "E": "Glutamic acid", "G": "Glycine",
    "H": "Histidine", "I": "Isoleucine", "L": "Leucine", "K": "Lysine",
    "M": "Methionine", "F": "Phenylalanine", "P": "Proline", "S": "Serine",
    "T": "Threonine", "W": "Tryptophan", "Y": "Tyrosine", "V": "Valine",
    "*": "Stop",
}


def codons_for(amino_acid: str):
    """Return all codons that code for a given amino acid."""
    aa = amino_acid.strip().upper()
    return [codon for codon, a in CODON_TABLE.items() if a == aa]


def degeneracy(amino_acid: str) -> int:
    """How many codons code for this amino acid (its degeneracy)."""
    return len(codons_for(amino_acid))


def synonymous_probability(amino_acid: str) -> float:
    """
    Exact synonymous-mutation probability.

    For each codon of this amino acid, count how many of the 9 possible
    single-base substitutions (3 positions x 3 alternative bases) produce
    a codon that still codes for the SAME amino acid. Average across codons.
    """
    aa = amino_acid.strip().upper()
    codons = codons_for(aa)
    if not codons:
        return 0.0

    bases = "UCAG"
    total_syn = 0
    total_mut = 0

    for codon in codons:
        for i in range(3):
            for b in bases:
                if b == codon[i]:
                    continue
                mutated = codon[:i] + b + codon[i+1:]
                total_mut += 1
                if CODON_TABLE.get(mutated) == aa:
                    total_syn += 1

    return total_syn / total_mut if total_mut else 0.0


def translate(sequence: str) -> str:
    """Translate an RNA (or DNA, T->U) sequence into a protein string."""
    seq = sequence.upper().strip().replace("T", "U")
    protein = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein.append(CODON_TABLE.get(codon, "?"))
    return "".join(protein)


def dna_match_probability(allele_frequencies):
    """
    Random match probability for a DNA profile.

    allele_frequencies: list of per-locus genotype probabilities (0-1).
    Multiplies them together to get the combined RMP.
    """
    rmp = 1.0
    for p in allele_frequencies:
        rmp *= p
    return rmp