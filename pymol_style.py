#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom styles for PyMOL."""

## IMPORT LIBRARIES
from pymol import cmd

# Bondi VDW values
bondi_vdw = {
    "Ac": 2.00, "Al": 2.00, "Am": 2.00, "Sb": 2.00, "Ar": 1.88, "As": 1.85,
    "At": 2.00, "Ba": 2.00, "Bk": 2.00, "Be": 2.00, "Bi": 2.00, "Bh": 2.00,
    "B":  2.00, "Br": 1.85, "Cd": 1.58, "Cs": 2.00, "Ca": 2.00, "Cf": 2.00,
    "C":  1.70, "Ce": 2.00, "Cl": 1.75, "Cr": 2.00, "Co": 2.00, "Cu": 1.40,
    "Cm": 2.00, "Ds": 2.00, "Db": 2.00, "Dy": 2.00, "Es": 2.00, "Er": 2.00,
    "Eu": 2.00, "Fm": 2.00, "F":  1.47, "Fr": 2.00, "Gd": 2.00, "Ga": 1.87,
    "Ge": 2.00, "Au": 1.66, "Hf": 2.00, "Hs": 2.00, "He": 1.40, "Ho": 2.00,
    "In": 1.93, "I":  1.98, "Ir": 2.00, "Fe": 2.00, "Kr": 2.02, "La": 2.00,
    "Lr": 2.00, "Pb": 2.02, "Li": 1.82, "Lu": 2.00, "Mg": 1.73, "Mn": 2.00,
    "Mt": 2.00, "Md": 2.00, "Hg": 1.55, "Mo": 2.00, "Nd": 2.00, "Ne": 1.54,
    "Np": 2.00, "Ni": 1.63, "Nb": 2.00, "N":  1.55, "No": 2.00, "Os": 2.00,
    "O":  1.52, "Pd": 1.63, "P":  1.80, "Pt": 1.72, "Pu": 2.00, "Po": 2.00,
    "K":  2.75, "Pr": 2.00, "Pm": 2.00, "Pa": 2.00, "Ra": 2.00, "Rn": 2.00,
    "Re": 2.00, "Rh": 2.00, "Rb": 2.00, "Ru": 2.00, "Rf": 2.00, "Sm": 2.00,
    "Sc": 2.00, "Sg": 2.00, "Se": 1.90, "Si": 2.10, "Ag": 1.72, "Na": 2.27,
    "Sr": 2.00, "S":  1.80, "Ta": 2.00, "Tc": 2.00, "Te": 2.06, "Tb": 2.00,
    "Tl": 1.96, "Th": 2.00, "Tm": 2.00, "Sn": 2.17, "Ti": 2.00, "W":  2.00,
    "U":  1.86, "V":  2.00, "Xe": 2.16, "Yb": 2.00, "Y":  2.00, "Zn": 1.39,
    "Zr": 2.00
}
print("Updating VDW radii...")
for element, vdw in bondi_vdw.items():
    cmd.alter(f"elem {element}", f"vdw={vdw:.2f}")
cmd.rebuild()

# Set default view
cmd.space("cmyk")
cmd.bg_color("white")
# cmd.viewport(800, 800)
cmd.set("depth_cue", 0)
cmd.set("orthoscopic", 0)

# Set default lighting (modified rubber)
cmd.set("ambient", 0.3)
cmd.set("reflect", 0.4)
cmd.set("direct", 0.3)
cmd.set("spec_direct", 0)
cmd.set("spec_direct_power", 55)
cmd.set("light_count", 6)
cmd.set("edit_light", 1)
cmd.set("spec_count", -1)
cmd.set("shininess", 10.)
cmd.set("spec_reflect", -0.01)
cmd.set("specular", 1)
cmd.set("specular_intensity", 0.5)
cmd.set("ambient_occlusion_mode", 0)
cmd.set("ambient_occlusion_scale", 25)
cmd.set("ambient_occlusion_smooth", 10)
cmd.set("power", 1)
cmd.set("reflect_power", 1)
cmd.set("two_sided_lighting", 1)

# Set default rendering settings
cmd.set("antialias", 2)
cmd.set("ray_shadow", 0)
cmd.set("line_smooth", 1)
cmd.set("ray_trace_mode", 1)
cmd.set("opaque_background", 1)
# cmd.set("ray_shadow_decay_factor", 0.1)
# cmd.set("ray_shadow_decay_range", 2)

# Turn on shaders
cmd.set("use_shaders", 1)
cmd.set("cgo_use_shader", 1)
cmd.set("dot_use_shader", 1)
cmd.set("dash_use_shader", 1)
cmd.set("line_use_shader", 1)
cmd.set("mesh_use_shader", 1)
cmd.set("stick_use_shader", 1)
cmd.set("ribbon_use_shader", 1)
cmd.set("sphere_use_shader", 1)
cmd.set("surface_use_shader", 1)
cmd.set("cartoon_use_shader", 1)
cmd.set("nonbonded_use_shader", 1)
cmd.set("nb_spheres_use_shader", 1)

# Set default on-screen rendering settings
cmd.set("valence", 0)
cmd.set("stick_ball", 1)
cmd.set("stick_h_scale", 1)
cmd.set("sphere_mode", 5)
cmd.set("dot_as_spheres", 1)
cmd.set("surface_quality", 2)
cmd.set("ribbon_sampling", 20)
cmd.set("cartoon_sampling", 20)
cmd.set("transparency_mode", 2)
cmd.set("dash_as_cylinders", 1)
cmd.set("line_as_cylinders", 1)
cmd.set("mesh_as_cylinders", 1)
cmd.set("stick_as_cylinders", 1)
cmd.set("render_as_cylinders", 1)
cmd.set("ribbon_as_cylinders", 1)
cmd.set("nonbonded_as_cylinders", 1)
cmd.set("alignment_as_cylinders", 1)
cmd.set("cartoon_nucleic_acid_as_cylinders", 1)
cmd.set("cartoon_transparency", 0)
cmd.set("cartoon_discrete_colors", 1)
cmd.set("cartoon_side_chain_helper", 1)

# Set default label settings
cmd.set("label_size", 24)
cmd.set("label_color", 1)
cmd.set("label_bg_color", 0)
cmd.set("label_bg_transparency", 0.8)
cmd.set("label_outline_color", 1)
cmd.set("label_position", [0, 2.5, 10])


"""
set cartoon_oval_length, 1
set cartoon_oval_width, 0.1
set stick_radius, 0.16
set stick_ball, on
set stick_ball_ratio, 1.1
set dash_gap, 0.50000
set dash_radius, 0.20000
set dash_width, 4
"""