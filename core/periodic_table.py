"""Lookup helper for the periodic table."""

from .elements import ELEMENTS


def get_element(symbol: str):
    """Return (name, mass) for a symbol, or None if unknown."""
    symbol = symbol.strip().capitalize()
    return ELEMENTS.get(symbol)


def list_all():
    """Return all symbols, sorted."""
    return sorted(ELEMENTS.keys())


def search(query: str):
    """Find elements whose name or symbol contains query (case-insensitive)."""
    query = query.lower()
    results = []
    for symbol, (name, mass) in ELEMENTS.items():
        if query in symbol.lower() or query in name.lower():
            results.append((symbol, name, mass))
    return results