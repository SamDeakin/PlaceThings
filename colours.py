from enum import Enum
from collections import namedtuple

# Constants for the percent that looks good to overlay boolean data onto a backing picture
DARK_OVERLAY_PERCENT = 0.2
LIGHT_OVERLAY_PERCENT = 0.2

def shift_dark(colour_value):
    # Shifts a colour value to be darker
    # The value should be between 0-255
    return int(colour_value * DARK_OVERLAY_PERCENT)

def shift_light(colour_value):
    # Shifts a colour value to be lighter
    # The value should also be between 0-255
    return int(colour_value * LIGHT_OVERLAY_PERCENT + 255 * (1 - LIGHT_OVERLAY_PERCENT))

def darker(r, g, b):
    return (shift_dark(r), shift_dark(g), shift_dark(b))

def lighter(r, g, b):
    return (shift_light(r), shift_light(g), shift_light(b))

class Colour(namedtuple('Colour', ['number', 'hex', 'r', 'g', 'b'])):
    def darker(self):
        return darker(self.r, self.g, self.b)
    def lighter(self):
        return lighter(self.r, self.g, self.b)
    def get_tuple(self):
        return (self.r, self.g, self.b)

NUMBER_OF_COLOURS = 16

Colours = {
    0: Colour(number=0, hex='#FFFFFF', r=0xFF, g=0xFF, b=0xFF),
    1: Colour(number=1, hex='#E4E4E4', r=0xE4, g=0xE4, b=0xE4),
    2: Colour(number=2, hex='#888888', r=0x88, g=0x88, b=0x88),
    3: Colour(number=3, hex='#222222', r=0x22, g=0x22, b=0x22),
    4: Colour(number=4, hex='#FFA7D1', r=0xFF, g=0xA7, b=0xD1),
    5: Colour(number=5, hex='#E50000', r=0xE5, g=0x00, b=0x00),
    6: Colour(number=6, hex='#E59500', r=0xE5, g=0x95, b=0x00),
    7: Colour(number=7, hex='#A06A42', r=0xA0, g=0x6A, b=0x42),
    8: Colour(number=8, hex='#E5D900', r=0xE5, g=0xD9, b=0x00),
    9: Colour(number=9, hex='#94E044', r=0x94, g=0xE0, b=0x44),
    10: Colour(number=10, hex='#02BE01', r=0x02, g=0xBE, b=0x01),
    11: Colour(number=11, hex='#00E5F0', r=0x00, g=0xE5, b=0xF0),
    12: Colour(number=12, hex='#0083C7', r=0x00, g=0x83, b=0xC7),
    13: Colour(number=13, hex='#0000EA', r=0x00, g=0x00, b=0xEA),
    14: Colour(number=14, hex='#E04AFF', r=0xE0, g=0x4A, b=0xFF),
    15: Colour(number=15, hex='#820080', r=0x82, g=0x00, b=0x80),
}
