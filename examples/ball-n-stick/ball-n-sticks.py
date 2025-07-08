#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd
from pymol import util
from pymol import preset
from typing import Optional


## Functions
def stylize_ball_and_stick(
        selection: str,
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
    
    # Set stick color and background
    cmd.set("stick_color", "black")
    if set_background:
        cmd.set("bg_rgb", [1, 1, 1])  # White background
    
    # Apply preset at the end (maintaining original function behavior)
    if use_preset:
        preset.ball_and_stick(selection)


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


## Extend PyMOL commands
cmd.extend("stylize_ball_and_stick", stylize_ball_and_stick)
