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
                selection1: str,
                selection2: str = "polymer",
                surface: bool = 0) -> None:
    """
    """
    cmd.hide("everything")
    cmd.show("cartoon")
    cmd.color("white", "polymer")
    cmd.color("atomic", "not elem C")
    if surface > 0:
        cmd.set("surface_type", 2)
        cmd.set("two_sided_lighting")
        cmd.set("surface_carve_cutoff", 4.5)
        cmd.set("surface_carve_normal_cutoff", -0.1)
        cmd.set("surface_carve_selection", selection1)
        cmd.show("surface", f"byres {selection2} within 8 of {selection1}")
        cmd.set("transparency", 0.5, selection2)
        cmd.set("surface_color", "white", selection2)
        cmd.unset("ray_shadows")

    cmd.show("sticks", selection1)
    cmd.show("sticks", f"byres {selection2} within 3.5 of {selection1}")

## Extend PyMOL commands
cmd.extend("stylize_binding_site", stylize_binding_site)
