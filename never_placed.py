# python3

from PIL import Image

from colours import Colours
from colours import darker
from colours import lighter
from utils import load_frequency

never_placed = Image.new('RGB', (1000, 1000))
never_placed_dark = Image.new('RGB', (1000, 1000))
never_placed_light = Image.new('RGB', (1000, 1000))

file = load_frequency()

# The second and third line should have x,y == -1
# We don't use either line
# The second line is totals
_line = next(file)
# The third line is counts of the highest number placed
_line = next(file)

for x, y, colour_data, final_colour in file:
    colour = Colours[final_colour]
    number_placed = sum(colour_data)

    if number_placed == 0:
        never_placed.putpixel((x, y), (255, 255, 255))
        never_placed_dark.putpixel((x, y), (255, 255, 255))
        never_placed_light.putpixel((x, y), (0, 0, 0))
    else:
        never_placed_dark.putpixel((x, y), colour.darker())
        never_placed_light.putpixel((x, y), colour.lighter())

never_placed.save('results/never-placed/never-placed.png')
never_placed_dark.save('results/never-placed/never-placed-dark.png')
never_placed_light.save('results/never-placed/never-placed-light.png')
