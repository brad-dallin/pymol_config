#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd
from pymol import util
from pymol import preset
from typing import Optional


## Functions
def _apply_element_colors(selection: str) -> None:
    """
    Apply standard CPK-like coloring scheme to molecular elements.
    
    Parameters:
    -----------
    selection : str
        PyMOL selection string
    """
    color_scheme = {
        "C": "gray85",    # Carbon - light gray
        "O": "red",       # Oxygen - red  
        "N": "slate",     # Nitrogen - blue-gray
        "H": "gray98",    # Hydrogen - near white
        "S": "yellow",    # Sulfur - yellow
        "P": "orange",    # Phosphorus - orange
    }
    for element, color in color_scheme.items():
        element_selection = f"{selection} and elem {element}"
        if cmd.count_atoms(element_selection):
            cmd.color(color, element_selection)


def _setup_plddt_colors(custom_colors: Optional[dict] = None) -> None:
    """
    Set up pLDDT color definitions in PyMOL.
    
    Parameters:
    -----------
    custom_colors : dict, optional
        Custom color definitions as RGB tuples (0-255 range)
    """
    # Default AlphaFold2 pLDDT colors (RGB 0-255 range)
    default_colors = {
        'very_high': (33, 81, 204),   # Dark blue - very confident
        'high': (127, 201, 239),      # Light blue - confident  
        'low': (249, 220, 77),        # Yellow - low confidence
        'very_low': (238, 132, 83)    # Orange - very low confidence
    }
    
    # Use custom colors if provided, otherwise use defaults
    colors = custom_colors if custom_colors else default_colors
    
    # Set PyMOL colors (convert from 0-255 to 0-1 range)
    for confidence_level, rgb in colors.items():
        color_name = f"plddt_{confidence_level}"
        rgb_normalized = [c / 255.0 for c in rgb]
        cmd.set_color(color_name, rgb_normalized)


def _get_plddt_color_name(
        b_factor: float,
        very_high_threshold: float,
        high_threshold: float,
        low_threshold: float) -> str:
    """
    Determine the appropriate pLDDT color name based on B-factor value.
    
    Parameters:
    -----------
    b_factor : float
        B-factor value (pLDDT score)
    very_high_threshold : float
        Threshold for very high confidence
    high_threshold : float
        Threshold for high confidence
    low_threshold : float
        Threshold for low confidence
    
    Returns:
    --------
    str
        PyMOL color name corresponding to the confidence level
    """
    if b_factor > very_high_threshold:
        return "plddt_very_high"
    elif b_factor > high_threshold:
        return "plddt_high"
    elif b_factor > low_threshold:
        return "plddt_low"
    else:
        return "plddt_very_low"


def stylize_ball_and_stick(selection: str,
                          stick_radius: float = 0.07,
                          sphere_scale: float = 0.18,
                          hydrogen_scale: float = 0.13,
                          stick_quality: int = 50,
                          sphere_quality: int = 4,
                          set_background: bool = True,
                          use_preset: bool = True) -> None:
    """
    Apply a customized ball and stick representation to a PyMOL selection.
    
    This function creates a ball and stick representation with custom sizing,
    coloring, and quality settings for molecular visualization. Can optionally
    use PyMOL's built-in preset as a base (maintaining original behavior).
    
    Parameters:
    -----------
    selection : str
        PyMOL selection string (e.g., molecule name, residue selection)
    stick_radius : float, optional
        Radius of stick bonds (default: 0.07)
    sphere_scale : float, optional
        Scale factor for atom spheres (default: 0.18)
    hydrogen_scale : float, optional
        Scale factor specifically for hydrogen atoms (default: 0.13)
    stick_quality : int, optional
        Quality/smoothness of stick rendering (default: 50)
    sphere_quality : int, optional
        Quality/smoothness of sphere rendering (default: 4)
    set_background : bool, optional
        Whether to set background to white (default: True)
    use_preset : bool, optional
        Whether to apply PyMOL's ball_and_stick preset at the end (default: True)
        This maintains the original function's behavior
    
    Returns:
    --------
    None
    
    Example:
    --------
    >>> stylize_ball_and_stick("protein")
    >>> stylize_ball_and_stick("resn ALA", stick_radius=0.1, sphere_scale=0.2)
    >>> stylize_ball_and_stick("ligand", use_preset=False)  # Skip preset application
    """
    
    # Validate selection exists
    if not cmd.count_atoms(selection):
        raise ValueError(f"No atoms found in selection: '{selection}'")
    
    # Clear existing representations
    cmd.hide("everything", selection)
    
    # Apply ball and stick representation
    cmd.show("sticks", selection)
    cmd.show("spheres", selection)
    
    # Set geometric properties
    cmd.set("stick_radius", stick_radius, selection)
    cmd.set("sphere_scale", sphere_scale, selection)
    cmd.set("sphere_scale", hydrogen_scale, f"{selection} and elem H")
    
    # Set rendering quality
    cmd.set("stick_quality", stick_quality, selection)
    cmd.set("sphere_quality", sphere_quality, selection)
    
    # Apply element-based coloring scheme
    _apply_element_colors(selection)
    
    # Apply preset at the end (maintaining original function behavior)
    if use_preset:
        preset.ball_and_stick(selection)

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
        cmd.set("two_sided_lighting")
    
    # Show stick representations for binding site
    cmd.show("sticks", selection1)
    cmd.show("sticks", f"byres {selection2} within 4 of {selection1}")


def color_by_plddt(
        selection: str,
        very_high_threshold: float = 90.0,
        high_threshold: float = 70.0,
        low_threshold: float = 50.0,
        custom_colors: Optional[dict] = None) -> None:
    """
    Color atoms by AlphaFold pLDDT (predicted Local Distance Difference Test) score.
    
    This function colors atoms based on their B-factor values, which in AlphaFold
    structures represent pLDDT confidence scores. Higher scores indicate higher
    confidence in the predicted structure.
    
    Parameters:
    -----------
    selection : str
        PyMOL selection string (e.g., molecule name, residue selection)
    very_high_threshold : float, optional
        Threshold for very high confidence coloring (default: 90.0)
    high_threshold : float, optional
        Threshold for high confidence coloring (default: 70.0)
    low_threshold : float, optional
        Threshold for low confidence coloring (default: 50.0)
    custom_colors : dict, optional
        Custom color definitions as RGB tuples (0-255 range)
        Keys: 'very_high', 'high', 'low', 'very_low'
    
    Returns:
    --------
    None
    
    Example:
    --------
    >>> color_by_plddt("alphafold_protein")
    >>> color_by_plddt("chain A", very_high_threshold=95.0, high_threshold=80.0)
    >>> custom_colors = {'very_high': (0, 255, 0), 'high': (255, 255, 0)}
    >>> color_by_plddt("protein", custom_colors=custom_colors)
    """
    
    # Validate selection exists
    if not cmd.count_atoms(selection):
        raise ValueError(f"No atoms found in selection: '{selection}'")
    
    # Validate thresholds
    if not (very_high_threshold > high_threshold > low_threshold):
        raise ValueError("Thresholds must be in descending order: very_high > high > low")
    
    # Set up color definitions
    _setup_plddt_colors(custom_colors)
    
    # Get atom indices and B-factors
    atom_data = []
    cmd.iterate(selection, 'atom_data.append((index, b))', space={'atom_data': atom_data})
    
    if not atom_data:
        raise ValueError(f"No B-factor data found for selection: '{selection}'")
    
    # Apply colors based on B-factor (pLDDT) values
    for atom_index, b_factor in atom_data:
        color_name = _get_plddt_color_name(
            b_factor,
            very_high_threshold,
            high_threshold,
            low_threshold
        )
        cmd.color(color_name, f"index {atom_index}")


# Extend PyMOL commands
cmd.extend("stylize_ball_and_stick", stylize_ball_and_stick)
cmd.extend("stylize_binding_site", stylize_binding_site)
cmd.extend("color_by_plddt", color_by_plddt)
