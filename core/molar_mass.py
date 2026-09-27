"""Molar mass calculator."""

import re
from .elements import ELEMENTS


def parse_formula(formula: str) -> dict:
    """Turn 'C6H12O6' into {'C': 6, 'H': 12, 'O': 6}."""
    pattern = r"([A-Z][a-z]?)(\d*)"
    counts = {}

    for symbol, number in re.findall(pattern, formula):
        if symbol not in ELEMENTS:
            raise ValueError(f"Unknown element: {symbol}")
        count = int(number) if number else 1
        counts[symbol] = counts.get(symbol, 0) + count

    return counts


def molar_mass(formula: str) -> float:
    """Return molar mass in g/mol."""
    counts = parse_formula(formula)
    total = 0.0
    for symbol, count in counts.items():
        _, mass = ELEMENTS[symbol]
        total += mass * count
    return total


def explain(formula: str) -> str:
    """Human-readable breakdown."""
    counts = parse_formula(formula)
    lines = [f"Formula: {formula}"]
    total = 0.0
    for symbol, count in counts.items():
        name, mass = ELEMENTS[symbol]
        subtotal = mass * count
        total += subtotal
        lines.append(f"  {symbol} ({name}): {count} x {mass} = {subtotal:.3f}")
    lines.append(f"Total: {total:.3f} g/mol")
    return "\n".join(lines)