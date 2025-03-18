#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd
from pymol import util


# Defines BallnStick settings
def ball_n_stick(arg1):
    cmd.show("sticks", arg1)
    cmd.show("spheres", arg1)
    cmd.color("atomic", f"(not elem C) and {arg1}")
    cmd.color("gray95", f"elem C and {arg1}")
    cmd.color("grey98", f"elem H and {arg1}")
    cmd.set("stick_radius", 0.07, arg1)
    cmd.set("sphere_scale", 0.18, arg1)
    cmd.set("sphere_scale", 0.13, f"{arg1} and elem H")
    cmd.set("dash_gap", 0.01, arg1)
    cmd.set("dash_radius", 0.07, arg1)
    cmd.set("stick_color", "black", arg1)
    cmd.set("dash_gap", 0.01)
    cmd.set("dash_radius", 0.035)
    cmd.hide("nonbonded", arg1)
    cmd.hide("lines", arg1)
    cmd.zoom(arg1)
    cmd.hide("labels")


def ball_n_stick_thick(arg1, color):
    cmd.show("licorice", arg1)
    cmd.show("spheres", arg1)
    cmd.unset("stick_color", arg1)
    util.cnc(arg1)
    cmd.color("atomic", f"(not elem C) and {arg1}")
    cmd.color(color, f"elem C and {arg1}")
    cmd.color("gray98", f"elem H and {arg1}")
    cmd.set("stick_radius", 0.17, arg1)
    cmd.set("sphere_scale", 0.18, arg1)
    cmd.set("dash_radius", 0.07, arg1)
    cmd.set("dash_gap", 0.05)
    cmd.set("dash_radius", 0.035)
    cmd.hide("nonbonded", arg1)
    cmd.hide("everything", f"{arg1} and elem H")
    cmd.zoom(arg1)


# Defines VDW Sphere settings
def add_vdw(arg1):
    vdw_object = f"{arg1}_vdw"
    cmd.copy(vdw_object, arg1)
    cmd.set("sphere_scale", 1.0, f"{vdw_object} and elem H")
    cmd.rebuild()
    cmd.set("sphere_scale", 1, vdw_object)
    cmd.hide("nonbonded", vdw_object)
    cmd.hide("lines", vdw_object)
    cmd.hide("sticks", vdw_object)
    cmd.set("sphere_transparency", 0.7, vdw_object)


# Defines protein settings for binding site
def pretty_binding_site():
    """
    Example:
        PyMOL> pretty_binding_site
    """
    cmd.show("sticks", "byres all within 3 of sele")
    cmd.color("pastel_pink", "elem C and not sele")
    cmd.hide("everything", "(hydro and (elem H and not (neighbor elem N+O)))")
    cmd.show("sticks", "sele")
    cmd.color("pastel_brown", "elem C and sele")
    cmd.set("cartoon_color", "grey98")
    cmd.hide("sticks", "backbone and (not name CA)")


# def set_pretty():
#     # Workspace settings
#     cmd.bg_color("white")
#     cmd.set("ray_opaque_background", "off")
#     cmd.set("orthoscopic", 0)
#     cmd.set("transparency", 0.5)
#     cmd.set("dash_gap", 0)
#     cmd.set("ray_trace_mode", 1)
#     cmd.set("antialias", 3)
#     cmd.set("ambient", 0.5)
#     cmd.set("spec_count", 5)
#     cmd.set("shininess", 50)
#     cmd.set("specular", 1)
#     cmd.set("reflect", 0.1)
#     cmd.space("cmyk")

def plddt_colors(arg1: str):
    """
    Color atoms by AF2 pLDDT score.
    """
    cmd.set_color("plddt_very_high", [33, 81, 204])
    cmd.set_color("plddt_high", [127, 201, 239])
    cmd.set_color("plddt_low", [249, 220, 77])
    cmd.set_color("plddt_very_low", [238, 132, 83])
    myspace = {'atom_index': []}
    cmd.iterate(arg1, 'atom_index.append((index, b))', space=myspace)
    for ii, bb in myspace['atom_index']:
        if bb > 90.:
            cmd.color("plddt_very_high", f"index {ii}")
        elif bb > 70.:
            cmd.color("plddt_high", f"index {ii}")
        elif bb > 50.:
            cmd.color("plddt_low", f"index {ii}")
        else:
            cmd.color("plddt_very_low", f"index {ii}")


# Extend PyMOL commands
cmd.extend("pretty_binding_site", pretty_binding_site)
# cmd.extend("set_pretty", set_pretty)
cmd.extend("ball_n_stick", ball_n_stick)
cmd.extend("ball_n_stick_thick", ball_n_stick_thick)
cmd.extend("add_vdw", add_vdw)
cmd.extend("plddt_colors", plddt_colors)
