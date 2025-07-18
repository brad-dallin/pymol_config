#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd


## Functions
def stylize_binding_site(
        selection1: str,
        selection2: str = "polymer",
        surface: str = "0") -> None:
    """
    Apply a customized binding site visualization to PyMOL selections.
    
    This function creates a binding site representation showing the main structure
    as cartoon, with sticks for the binding site and nearby residues. Optionally
    displays a carved surface around the binding site.
    
    Parameters:
    -----------
    selection1 : str
        PyMOL selection string for the binding site/ligand
    selection2 : str, optional
        PyMOL selection string for the main structure (default: "polymer")
    surface : str, optional
        Whether to show surface representation ("0" for no surface, "1" for surface)
        (default: "0")
    
    Returns:
    --------
    None
    
    Example:
    --------
    >>> stylize_binding_site("ligand", "protein")
    >>> stylize_binding_site("resn ATP", "chain A", surface="1")
    """
    
    # Validate selections exist
    if not cmd.count_atoms(selection1):
        raise ValueError(f"No atoms found in selection1: '{selection1}'")
    if not cmd.count_atoms(selection2):
        raise ValueError(f"No atoms found in selection2: '{selection2}'")
    
    # Clear existing representations
    cmd.hide("everything")
    
    # Show cartoon representation for main structure
    cmd.show("cartoon")
    cmd.color("cb_lightblue", "polymer")
    cmd.color("atomic", "not elem C")
    
    # Configure surface if requested
    if int(surface) > 0:
        cmd.set("surface_type", 2)
        cmd.set("surface_carve_cutoff", 4.5)
        cmd.set("surface_carve_normal_cutoff", -0.1)
        cmd.set("surface_carve_selection", selection1)
        cmd.show("surface", f"byres {selection2} within 8 of {selection1}")
        cmd.set("transparency", 0.5, selection2)
        cmd.set("surface_color", "white", selection2)
        cmd.set("two_sided_lighting", 1)
    
    # Show stick representations for binding site
    cmd.show("sticks", selection1)
    cmd.show("sticks", f"byres {selection2} within 4 of {selection1}")

## Extend PyMOL commands
cmd.extend("stylize_binding_site", stylize_binding_site)
