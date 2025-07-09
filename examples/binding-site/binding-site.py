#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd
# from pymol import util
# from pymol import preset
# from typing import Optional


## Functions
def stylize_binding_site(
        selection: str,
        receptor: str = "polymer") -> None:
    """
    """
    cmd.set("surface_carve_cutoff", 4.5)
    cmd.set("surface_carve_selection", selection)
    cmd.set("surface_carve_normal_cutoff", -0.1)

    cmd.show("surface", f"{receptor} within 8 of {selection}")
    cmd.set("two_sided_lighting")
    cmd.set("transparency", 0.5)
    cmd.show("sticks", selection)
    cmd.orient(selection)

    # cmd.set("surface_color", "white")
    cmd.set("surface_type", 2)
    cmd.unset("ray_shadows")

## Extend PyMOL commands
cmd.extend("stylize_binding_site", stylize_binding_site)
