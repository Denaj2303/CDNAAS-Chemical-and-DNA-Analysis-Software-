"""Fetch molecular structures from PubChem and render them with py3Dmol."""

import math
import requests
import py3Dmol


PUBCHEM_URL = (
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
    "{name}/SDF?record_type=3d"
)


def fetch_structure(name: str) -> str:
    """
    Fetch the 3D SDF structure of a molecule by name from PubChem.
    Returns the SDF text. Raises ValueError if not found.
    """
    name = name.strip()
    if not name:
        raise ValueError("Empty molecule name.")

    url = PUBCHEM_URL.format(name=requests.utils.quote(name))
    response = requests.get(url, timeout=15)

    if response.status_code == 404:
        raise ValueError(f"Molecule not found: {name}")
    if response.status_code != 200:
        raise ValueError(
            f"PubChem error {response.status_code}: {response.text[:120]}"
        )

    return response.text


def render_molecule(name: str, style: str = "stick") -> None:
    """
    Fetch a molecule by name and open a 3D view in the browser.

    style: 'stick', 'sphere', 'line', or 'cartoon'
    """
    sdf = fetch_structure(name)

    view = py3Dmol.view(width=800, height=600)
    view.addModel(sdf, "sdf")

    if style == "sphere":
        view.setStyle({"sphere": {"scale": 0.4}})
    elif style == "line":
        view.setStyle({"line": {}})
    elif style == "cartoon":
        view.setStyle({"cartoon": {"color": "spectrum"}})
    else:  # stick (default)
        view.setStyle({"stick": {"radius": 0.15}, "sphere": {"scale": 0.25}})

    view.setBackgroundColor("black")
    view.zoomTo()
    view.show()


def render_dna_helix(sequence: str) -> None:
    """
    Render a stylized 3D DNA double helix from a sequence (A, T, G, C).
    This is a geometric representation, not an atomic structure.
    """
    sequence = sequence.upper().strip()
    if not sequence:
        raise ValueError("Empty DNA sequence.")

    view = py3Dmol.view(width=800, height=600)
    view.setBackgroundColor("black")

    radius = 5.0
    rise = 1.5       # vertical distance per base
    twist = 36       # degrees per base (10 bases per turn)

    color_map = {"A": "green", "T": "red", "G": "blue", "C": "yellow"}
    pair_map = {"A": "red", "T": "green", "G": "yellow", "C": "blue"}

    for i, base in enumerate(sequence):
        angle = math.radians(i * twist)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = i * rise

        color = color_map.get(base, "white")

        view.addSphere({
            "center": {"x": x, "y": y, "z": z},
            "radius": 0.7,
            "color": color,
            "alpha": 0.9,
        })

        x2, y2 = -x, -y
        view.addSphere({
            "center": {"x": x2, "y": y2, "z": z},
            "radius": 0.7,
            "color": pair_map.get(base, "gray"),
            "alpha": 0.9,
        })

        view.addLine({
            "start": {"x": x, "y": y, "z": z},
            "end": {"x": x2, "y": y2, "z": z},
            "color": "gray",
        })

    view.zoomTo()
    view.show()