# python3

from PIL import Image

from colours import Colours
from colours import darker
from colours import lighter
from colours import NUMBER_OF_COLOURS
from utils import load_frequency

colour_files = [Image.new('RGB', (1000, 1000)) for _ in NUMBER_OF_COLOURS]
colour_json = [{'data': {}, 'total': 0} for _ in NUMBER_OF_COLOURS]
total_file = Image.new('RGB', (1000, 1000))

file = load_frequency()

# The Second and Third line have x,y == -1
# The Second line is totals, which we don't need here
_line = next(file)

# The Third line is the highest of each colour in a singe pixel, which we must save
_x, _y, highest_by_colour, highest_total = next(file)

for c, num in enumerate(highest_by_colour, 0):
    # Save the highest values in the json structures
    colour_json[c]['total'] = num

def adjust_colour(colour_tuple, frequency, total_frequency):
    # Adjusts colour_tuple based on frequency / total_frequency
    fraction = frequency / total_frequency
    return tuple([int(value * fraction) for value in colour_tuple])

for x, y, colour_data, final_colour in file:
    colour = Colours[final_colour]
    total_placed = sum(colour_data)

    total_file.putpixel(
        (x, y),
        adjust_colour(
            colour.get_tuple(),
            total_placed,
            highest_total,
        ),
    )

""" Ideas
Add csv files of frequencies
    Allow element where users can select colours they want to view, then combine them by selecting multiple
