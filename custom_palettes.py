#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module providing custom color palettes for PyMOL."""

# IMPORT LIBRARIES
from __future__ import print_function
import math
from typing import Optional
from typing import NamedTuple

# IMPORT PYMOL MODULES
import pymol
from pymol import cmd


# PALETTE COLOR CLASS
class PaletteColor(NamedTuple):
    """Named tuple for storing color information."""
    name: str
    rgb: tuple[int, int, int]
    alt_names: Optional[list[str]] = None 
    # NOTE: Allow the short_code to be set explicitly in the palette definition. This is helpful
    # for very dark colors, as it ensures that the color code used in the GUI menu provides
    # sufficient contrast against the dark menu background, making the colors more distinguishable.
    short_code: Optional[str] = None # 3-digit string approximating the RGB color

    def all_names(self):
        """Return a list of all names for this color."""
        names = [self.name]
        if self.alt_names:
            names.extend(self.alt_names)
        return names

    def get_short_code(self):
        """Return a 3-digit string approximating the RGB color."""
        if self.short_code:
            return self.short_code
        return ''.join(str(math.floor(x / 256 * 10)) for x in self.rgb)

# PALETTE CLASS
class Palette(NamedTuple):
    """Named tuple for storing palette information."""
    name: str
    colors: list[PaletteColor]
    prefix: str = ''

    def install(self):
        """Install the palette, adding colors and the GUI menu."""
        PALETTES_MAP[self.name] = self
        add_menu(self.name)


def _get_palettes(palette_name: Optional[str] = None):
    """Return the desired Palette(s)."""
    if palette_name is None:
        return PALETTES_MAP.values()
    if palette_name not in PALETTES_MAP:
        raise ValueError(f'Palette "{palette_name}" not found.')
    return [PALETTES_MAP[palette_name]]


def set_colors(palette=None, replace=False):
    """Add the palette colors to PyMOL."""
    palettes = _get_palettes(palette)
    for palette in palettes:
        max_name_length = max(len(c.name) for c in palette.colors)
        added_colors = []
        for color in palette.colors:
            rgb = color.rgb

            # Set the colors
            for name in color.all_names():
                if palette.prefix:
                    use_name = f'{palette.prefix}{name}'
                else:
                    use_name = name
                cmd.set_color(use_name, rgb)

                # Optionally replace built-in colors
                if replace:
                    cmd.set_color(name, rgb)
                    spacer = (max_name_length - len(name) + 4) * ' '
                    added_colors.append(f'    {name}{spacer}{use_name}')
                else:
                    added_colors.append(f'    {use_name}')

        # Notify user of newly available colors
        print(f'These {palette.name} colors are now available:')
        print('\n'.join(added_colors))


def _add_palette_menu(palette: Palette):
    """Add a color palette to the PyMOL OpenGL menu."""

    # Make sure colors are installed.
    print(f'Checking for {palette.name} colors...')
    try:
        for color in palette.colors:
            if cmd.get_color_index(color.name) == -1:
                # mimic pre-1.7.4 behavior
                raise pymol.CmdException
    except pymol.CmdException:
        print(f'Adding {palette.name} palette colors...')
        set_colors(palette=palette.name)

    # Add the menu
    print(f'Adding {palette.name} menu...')
    # mimic pymol.menu.all_colors_list format
    # first color in list is used for menu item color

    # Menu item for each color in the menu should be a tuple in the form
    #    ('999', 'color_name')
    # where '999' is a string representing the 0-255 RGB color converted to
    # a 0-9 integer RGB format (i.e. 1000 colors).
    color_tuples = [
        (color.get_short_code(), palette.prefix + color.name)
        for color in palette.colors
    ]
    menu_colors = (palette.name, color_tuples)

    # First `pymol` is the program instance, second is the Python module
    # Abort if PyMOL is too old.
    try:
        all_colors = pymol.pymol.menu.all_colors_list
    except ImportError:
        print("PyMOL version too old for colors menu. Requires 1.6.0 or later.")
        return
    if menu_colors in all_colors:
        print(f'  - Menu for {palette.name} was already added!')
    else:
        all_colors.append(menu_colors)
    print('    done.\n')


def add_menu(palette_name=None):
    """Add the specified color palettes to the PyMOL OpenGL menu."""
    palettes = _get_palettes(palette_name)
    for palette in palettes:
        _add_palette_menu(palette)


def remove_menu(palette_name=None):
    """Remove the color palette menu(s)."""
    palettes = _get_palettes(palette_name)
    all_colors_list = pymol.pymol.menu.all_colors_list
    for palette in palettes:
        initial_length = len(all_colors_list)
        all_colors_list[:] = [
            color_menu for color_menu in all_colors_list
            if color_menu[0] != palette.name
        ]
        if len(all_colors_list) == initial_length:
            print(f'No menu for {palette.name} palette found. Nothing deleted.')
        else:
            print(f'Deleted menu for {palette.name} palette.')


## COLOR PALETTES
PASTEL_COLORS = [
    PaletteColor('pastel_blue',   (169, 200, 240)),
    PaletteColor('pastel_orange', (244, 183, 138)),
    PaletteColor('pastel_green',  (161, 227, 167)),
    PaletteColor('pastel_red',    (255, 104, 138)),
    PaletteColor('pastel_purple', (204, 188, 250)),
    PaletteColor('pastel_brown',  (216, 188, 159)),
    PaletteColor('pastel_pink',   (239, 179, 225)),
    PaletteColor('pastel_grey',   (207, 207, 207)),
    PaletteColor('pastel_yellow', (255, 254, 174)),
    PaletteColor('pastel_teal',   (197, 240, 239)),
]
CB_COLORS = [
    PaletteColor('cb_red',       (213,  94,   0)),
    PaletteColor('cb_orange',    (230, 159,   0)),
    PaletteColor('cb_yellow',    (240, 228,  66)),
    PaletteColor('cb_green',     (  0, 158, 115)),
    PaletteColor('cb_blue',      (  0, 114, 178)),
    PaletteColor('cb_lightblue', ( 86, 180, 233)),
    PaletteColor('cb_violet',    (204, 121, 167)),
    PaletteColor('cb_black',       (0,   0,   0), short_code='222'),
]
VIRIDIS_COLORS = [
    PaletteColor('viridis1',  (253, 231,  36)),
    PaletteColor('viridis2',  (186, 222,  39)),
    PaletteColor('viridis3',  (121, 209,  81)),
    PaletteColor('viridis4',  ( 66, 190, 113)),
    PaletteColor('viridis5',  ( 34, 167, 132)),
    PaletteColor('viridis6',  ( 32, 143, 140)),
    PaletteColor('viridis7',  ( 41, 120, 142)),
    PaletteColor('viridis8',  ( 52,  94, 141)),
    PaletteColor('viridis9',  ( 64,  67, 135)),
    PaletteColor('viridis10', ( 72,  35, 116)),
    PaletteColor('viridis11', ( 68,   1,  84)),
]
MAGMA_COLORS = [
    PaletteColor('magma1',  (251, 252, 191)),
    PaletteColor('magma2',  (253, 205, 114)),
    PaletteColor('magma3',  (253, 159, 108)),
    PaletteColor('magma4',  (246, 110,  91)),
    PaletteColor('magma5',  (221,  73, 104)),
    PaletteColor('magma6',  (181,  54, 121)),
    PaletteColor('magma7',  (140,  41, 128)),
    PaletteColor('magma8',  ( 99,  25, 127)),
    PaletteColor('magma9',  ( 59,  15, 111)),
    PaletteColor('magma10', ( 20,  13,  53)),
    PaletteColor('magma11', (  0,   0,   3)),
]
PASTEL_PALETTE = Palette('pastel', PASTEL_COLORS)
CB_PALETTE = Palette('colorblind', CB_COLORS)
VIRIDIS_PALETTE = Palette('viridis', VIRIDIS_COLORS)
MAGMA_PALETTE = Palette('magma', MAGMA_COLORS)

PALETTES_MAP = {
    PASTEL_PALETTE.name: PASTEL_PALETTE,
    CB_PALETTE.name: CB_PALETTE,
    VIRIDIS_PALETTE.name: VIRIDIS_PALETTE,
    MAGMA_PALETTE.name: MAGMA_PALETTE,
}

if __name__ == "pymol":
    add_menu()
