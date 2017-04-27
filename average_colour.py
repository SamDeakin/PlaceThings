# python3
import shutil
import traceback

from PIL import Image

from colours import Colours
from colours import NUMBER_OF_COLOURS
from colours import darker
from colours import lighter

print('Setting up...')

# The number of lines in tile_placements.csv
# This is hardcoded because there's no way to get it without reading the entire file
# and it will only be used for the progress bar
NUM_LINES = 16559898
NUM_PIXELS = 1000 * 1000

def print_progress(num, total):
    percent = num / total
    columns = 50
    bar = '#' * int((columns - 2) * percent) + '-' * int((columns - 2) * (1 - percent))
    print('[{bar}] {percent:.2f}%'.format(bar=bar, percent=percent * 100), end='\r')

pixels = [[[0 for i in range(NUMBER_OF_COLOURS)] for j in range(1000)] for k in range(1000)]
final_pixel = [[(0, 0) for i in range(1000)] for k in range(1000)]

print('Processing file...')

with open('tile_placements.csv') as f:

    # Read the line with the column names
    line = f.readline()

    for line_num, line in enumerate(f, 1):
        timestamp, user, x, y, colour = line.split(sep=',')
        try:
            x = int(x) - 1
            y = int(y) - 1
            colour = int(colour)
            timestamp = int(timestamp)

            pixels[x][y][colour] += 1

            current_timestamp, current_colour = final_pixel[x][y]
            if timestamp > current_timestamp:
                final_pixel[x][y] = (timestamp, colour)

            print_progress(line_num, NUM_LINES)
        except:
            traceback.print_exc()
            print('Error at line {num}: "{line}"'.format(num=line_num, line=line.strip()))
            exit(line_num)

# Add a newline at the end
print()

print('Creating images...')

# We create two images here
# This is average colour with colours weighted by blending
blended_average = Image.new('RGB', (1000, 1000), color=(255, 255, 255))
# This is the most common colour
most_common = Image.new('RGB', (1000, 1000), color=(255, 255, 255))

# This is for pixels that were never placed
never_placed = Image.new('RGB', (1000, 1000))
# More never placed data with the end result overlaid on top
never_placed_dark_overlay = Image.new('RGB', (1000, 1000))
never_placed_light_overlay = Image.new('RGB', (1000, 1000))

for x in range(1000):
    for y in range(1000):
        most = [-1]
        most_num = -1
        total_placed = 0
        total_r = 0
        total_g = 0
        total_b = 0

        for c in range(NUMBER_OF_COLOURS):
            num = pixels[x][y][c]
            # Two cases to support mutliple colours of the same number placed
            if num == most_num:
                most += [c]
            if num > most_num:
                most_num = num
                most = [c]

            colour = Colours[c]
            total_placed += num
            total_r += colour.r * num
            total_g += colour.g * num
            total_b += colour.b * num

        if total_placed != 0:
            r = int(total_r / total_placed)
            g = int(total_g / total_placed)
            b = int(total_b / total_placed)
            blended_average.putpixel((x, y), (r, g, b))

        if most_num > 0:
            # Sum and average the colours with the (same) highest number of placements
            r = 0
            g = 0
            b = 0
            for c in most:
                colour = Colours[c]
                r += colour.r
                g += colour.g
                b += colour.b

            length = len(most)
            r = int(r / length)
            g = int(g / length)
            b = int(b / length)
            most_common.putpixel((x, y), (r, g, b))

            # Calculate the shifted final colour for the overlaid never_paced pictures
            timestamp, final_colour_code = final_pixel[x][y]
            final_colour = Colours[final_colour_code]
            final_r = final_colour.r
            final_g = final_colour.g
            final_b = final_colour.b

            never_placed_dark_overlay.putpixel((x, y), darker(final_r, final_g, final_b))
            never_placed_light_overlay.putpixel((x, y), lighter(final_r, final_g, final_b))
        else:
            never_placed.putpixel((x, y), (255, 255, 255))
            never_placed_dark_overlay.putpixel((x, y), (255, 255, 255))
            never_placed_light_overlay.putpixel((x, y), (0, 0, 0))

        print_progress(x * 1000 + y, NUM_PIXELS)

print()

blended_average.save('results/blended_average.png')
most_common.save('results/most_common.png')
never_placed.save('results/never_placed.png')
never_placed_dark_overlay.save('results/never_placed_dark_overlay.png')
never_placed_light_overlay.save('results/never_placed_light_overlay.png')
