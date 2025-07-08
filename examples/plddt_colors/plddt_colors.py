#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd
from typing import Optional


## Functions
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


## Extend PyMOL commands
cmd.extend("color_by_plddt", color_by_plddt)
