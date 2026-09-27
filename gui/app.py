"""Detective Mode - analysis console GUI."""

import customtkinter as ctk

from core.molar_mass import explain as mm_explain, molar_mass
from core.periodic_table import get_element, list_all, search as pt_search
from core.dna_tools import reverse_complement, gc_content, transcribe, count_bases
from core.genetics import (
    codons_for, degeneracy, synonymous_probability, translate,
    dna_match_probability, AA_NAMES,
)
from core.molecules import render_molecule, render_dna_helix


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Detective Mode")
        self.geometry("820x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()

        self.show_tool("Molar Mass")

    # ---------- Sidebar ----------
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="DETECTIVE\nMODE",
            font=("Courier", 18, "bold"),
        )
        title.pack(pady=(24, 20))

        self.tools = [
            "Molar Mass",
            "Periodic Table",
            "DNA Tools",
            "Genetics",
            "3D Viewer",
            "About",
        ]
        self.tool_buttons = {}

        for tool in self.tools:
            btn = ctk.CTkButton(
                self.sidebar,
                text=tool,
                command=lambda t=tool: self.show_tool(t),
                fg_color="transparent",
                anchor="w",
            )
            btn.pack(pady=4, padx=12, fill="x")
            self.tool_buttons[tool] = btn

    # ---------- Content ----------
    def _build_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_tool(self, tool: str):
        for widget in self.content.winfo_children():
            widget.destroy()

        for name, btn in self.tool_buttons.items():
            btn.configure(fg_color=("#1E88E5" if name == tool else "transparent"))

        if tool == "Molar Mass":
            self._render_molar_mass()
        elif tool == "Periodic Table":
            self._render_periodic_table()
        elif tool == "DNA Tools":
            self._render_dna_tools()
        elif tool == "Genetics":
            self._render_genetics()
        elif tool == "3D Viewer":
            self._render_3d_viewer()
        elif tool == "About":
            self._render_about()

    # ---------- Tool: Molar Mass ----------
    def _render_molar_mass(self):
        ctk.CTkLabel(self.content, text="MOLAR MASS",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            self.content, text="Enter a chemical formula (e.g. C6H12O6)",
            font=("Courier", 11), text_color="gray",
        ).pack(anchor="w", pady=(0, 12))

        entry = ctk.CTkEntry(self.content, placeholder_text="Formula", width=360,
                             font=("Courier", 14))
        entry.pack(anchor="w", pady=4)

        out = ctk.CTkTextbox(self.content, width=520, height=280, font=("Courier", 12))
        out.pack(anchor="w", pady=16, fill="both", expand=True)

        def run(_=None):
            out.delete("1.0", "end")
            formula = entry.get().strip()
            if not formula:
                out.insert("end", "Enter a formula first.\n")
                return
            try:
                out.insert("end", mm_explain(formula) + "\n")
                out.insert("end", f"\n>>> {molar_mass(formula):.3f} g/mol\n")
            except ValueError as e:
                out.insert("end", f"ERROR: {e}\n")

        ctk.CTkButton(self.content, text="ANALYZE", command=run, width=360,
                      font=("Courier", 13, "bold")).pack(anchor="w")
        entry.bind("<Return>", run)

    # ---------- Tool: Periodic Table ----------
    def _render_periodic_table(self):
        ctk.CTkLabel(self.content, text="PERIODIC TABLE",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            self.content, text="Search by symbol or name — leave blank to list all",
            font=("Courier", 11), text_color="gray",
        ).pack(anchor="w", pady=(0, 12))

        entry = ctk.CTkEntry(self.content, placeholder_text="e.g. Fe or iron",
                             width=360, font=("Courier", 14))
        entry.pack(anchor="w", pady=4)

        scroll = ctk.CTkScrollableFrame(self.content, width=520, height=300)
        scroll.pack(anchor="w", pady=16, fill="both", expand=True)

        def render(rows):
            for w in scroll.winfo_children():
                w.destroy()
            if not rows:
                ctk.CTkLabel(scroll, text="No matches.",
                             font=("Courier", 12)).pack(anchor="w")
                return
            for sym, name, mass in rows:
                line = ctk.CTkLabel(
                    scroll,
                    text=f"{sym:<3}  {name:<14}  {mass:>9.4f}",
                    font=("Courier", 13),
                    anchor="w",
                )
                line.pack(anchor="w", pady=1)

        def run(_=None):
            q = entry.get().strip()
            if not q:
                rows = [(s, *get_element(s)) for s in list_all()]
            else:
                rows = pt_search(q)
            render(rows)

        ctk.CTkButton(self.content, text="SEARCH", command=run, width=360,
                      font=("Courier", 13, "bold")).pack(anchor="w")
        entry.bind("<Return>", run)
        run()

    # ---------- Tool: DNA ----------
    def _render_dna_tools(self):
        ctk.CTkLabel(self.content, text="DNA TOOLS",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            self.content, text="Enter a DNA sequence (A, T, G, C)",
            font=("Courier", 11), text_color="gray",
        ).pack(anchor="w", pady=(0, 12))

        entry = ctk.CTkEntry(self.content, placeholder_text="e.g. ATGCGTAC",
                             width=520, font=("Courier", 14))
        entry.pack(anchor="w", pady=4)

        out = ctk.CTkTextbox(self.content, width=520, height=280, font=("Courier", 12))
        out.pack(anchor="w", pady=16, fill="both", expand=True)

        def run(_=None):
            out.delete("1.0", "end")
            seq = entry.get().strip()
            if not seq:
                out.insert("end", "Enter a DNA sequence.\n")
                return
            try:
                out.insert("end", f"Sequence:           {seq.upper()}\n")
                out.insert("end", f"Reverse complement: {reverse_complement(seq)}\n")
                out.insert("end", f"RNA transcript:     {transcribe(seq)}\n")
                out.insert("end", f"GC content:         {gc_content(seq):.2f}%\n\n")
                counts = count_bases(seq)
                out.insert("end", "Base counts:\n")
                for base, n in counts.items():
                    out.insert("end", f"  {base}: {n}\n")
            except ValueError as e:
                out.insert("end", f"ERROR: {e}\n")

        ctk.CTkButton(self.content, text="ANALYZE", command=run, width=520,
                      font=("Courier", 13, "bold")).pack(anchor="w")
        entry.bind("<Return>", run)

    # ---------- Tool: Genetics ----------
    def _render_genetics(self):
        ctk.CTkLabel(self.content, text="GENETICS",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            self.content,
            text="Codon degeneracy, translation, and match probability",
            font=("Courier", 11), text_color="gray",
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(self.content, text="Amino acid (single letter, e.g. L):",
                     font=("Courier", 12)).pack(anchor="w")
        aa_entry = ctk.CTkEntry(self.content, width=120, font=("Courier", 14))
        aa_entry.pack(anchor="w", pady=4)

        ctk.CTkLabel(self.content, text="DNA/RNA sequence to translate:",
                     font=("Courier", 12)).pack(anchor="w", pady=(12, 0))
        seq_entry = ctk.CTkEntry(self.content, width=520, font=("Courier", 14))
        seq_entry.pack(anchor="w", pady=4)

        ctk.CTkLabel(self.content,
                     text="Allele frequencies (comma-separated, e.g. 0.1,0.05,0.2):",
                     font=("Courier", 12)).pack(anchor="w", pady=(12, 0))
        freq_entry = ctk.CTkEntry(self.content, width=520, font=("Courier", 14))
        freq_entry.pack(anchor="w", pady=4)

        out = ctk.CTkTextbox(self.content, width=520, height=200, font=("Courier", 12))
        out.pack(anchor="w", pady=16, fill="both", expand=True)

        def run(_=None):
            out.delete("1.0", "end")

            aa = aa_entry.get().strip().upper()
            if aa:
                try:
                    codons = codons_for(aa)
                    if not codons:
                        out.insert("end", f"Unknown amino acid: {aa}\n\n")
                    else:
                        name = AA_NAMES.get(aa, aa)
                        d = degeneracy(aa)
                        p = synonymous_probability(aa)
                        out.insert("end", f"Amino acid: {aa} ({name})\n")
                        out.insert("end", f"Degeneracy: {d} codons\n")
                        out.insert("end", f"Codons: {', '.join(codons)}\n")
                        out.insert("end",
                                   f"Synonymous mutation probability: {p*100:.1f}%\n\n")
                except Exception as e:
                    out.insert("end", f"AA error: {e}\n\n")

            seq = seq_entry.get().strip()
            if seq:
                try:
                    protein = translate(seq)
                    out.insert("end", f"Sequence: {seq.upper()}\n")
                    out.insert("end", f"Protein:  {protein}\n\n")
                except Exception as e:
                    out.insert("end", f"Translate error: {e}\n\n")

            freqs = freq_entry.get().strip()
            if freqs:
                try:
                    values = [float(x) for x in freqs.split(",") if x.strip()]
                    rmp = dna_match_probability(values)
                    out.insert("end", f"Loci used: {len(values)}\n")
                    out.insert("end", f"Random match probability: {rmp:.3e}\n")
                    if rmp > 0:
                        out.insert("end", f"= 1 in {1/rmp:,.0f}\n")
                except Exception as e:
                    out.insert("end", f"RMP error: {e}\n")

        ctk.CTkButton(self.content, text="ANALYZE", command=run, width=520,
                      font=("Courier", 13, "bold")).pack(anchor="w")
        for e in (aa_entry, seq_entry, freq_entry):
            e.bind("<Return>", run)

    # ---------- Tool: 3D Viewer ----------
    def _render_3d_viewer(self):
        ctk.CTkLabel(self.content, text="3D VIEWER",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            self.content,
            text="Renders in your browser. Real molecules from PubChem.",
            font=("Courier", 11), text_color="gray",
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(self.content, text="Molecule name (e.g. caffeine, aspirin):",
                     font=("Courier", 12)).pack(anchor="w")
        mol_entry = ctk.CTkEntry(self.content, width=360, font=("Courier", 14))
        mol_entry.pack(anchor="w", pady=4)

        style_var = ctk.StringVar(value="stick")
        style_row = ctk.CTkFrame(self.content, fg_color="transparent")
        style_row.pack(anchor="w", pady=4)
        ctk.CTkLabel(style_row, text="Style:",
                     font=("Courier", 12)).pack(side="left", padx=(0, 8))
        for s in ("stick", "sphere", "line"):
            ctk.CTkRadioButton(style_row, text=s, variable=style_var, value=s,
                               font=("Courier", 12)).pack(side="left", padx=6)

        ctk.CTkLabel(self.content, text="Or: DNA sequence for a 3D helix:",
                     font=("Courier", 12)).pack(anchor="w", pady=(16, 0))
        dna_entry = ctk.CTkEntry(self.content, width=460, font=("Courier", 14))
        dna_entry.pack(anchor="w", pady=4)

        out = ctk.CTkTextbox(self.content, width=520, height=120, font=("Courier", 12))
        out.pack(anchor="w", pady=16, fill="both", expand=True)

        def render_mol():
            out.delete("1.0", "end")
            name = mol_entry.get().strip()
            if not name:
                out.insert("end", "Enter a molecule name first.\n")
                return
            out.insert("end", f"Fetching '{name}' from PubChem...\n")
            self.update_idletasks()
            try:
                render_molecule(name, style=style_var.get())
                out.insert("end", "Opened in browser. Rotate with your mouse.\n")
            except Exception as e:
                out.insert("end", f"ERROR: {e}\n")

        def render_dna():
            out.delete("1.0", "end")
            seq = dna_entry.get().strip()
            if not seq:
                out.insert("end", "Enter a DNA sequence first.\n")
                return
            try:
                render_dna_helix(seq)
                out.insert("end", f"Rendered helix for {len(seq)} bases.\n")
            except Exception as e:
                out.insert("end", f"ERROR: {e}\n")

        btn_row = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_row.pack(anchor="w", pady=4)

        ctk.CTkButton(btn_row, text="RENDER MOLECULE", command=render_mol,
                      width=200, font=("Courier", 12, "bold")).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="RENDER DNA HELIX", command=render_dna,
                      width=200, font=("Courier", 12, "bold")).pack(side="left")

        mol_entry.bind("<Return>", lambda e: render_mol())
        dna_entry.bind("<Return>", lambda e: render_dna())

    # ---------- Tool: About ----------
    def _render_about(self):
        ctk.CTkLabel(self.content, text="ABOUT",
                     font=("Courier", 20, "bold")).pack(anchor="w")
        text = (
            "Detective Mode - Lab Toolkit\n\n"
            "A forensic-style analysis console.\n\n"
            "Tools:\n"
            "  - Molar Mass Calculator\n"
            "  - Periodic Table (all 118 elements)\n"
            "  - DNA Sequence Analysis\n"
            "  - Genetics (codon degeneracy, translation, RMP)\n"
            "  - 3D Viewer (molecules from PubChem, DNA helix)\n\n"
            "Built with Python + CustomTkinter."
        )
        ctk.CTkLabel(self.content, text=text, font=("Courier", 12),
                     justify="left").pack(anchor="w", pady=12)