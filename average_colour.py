# python3
import shutil
import traceback

from PIL import Image

from colours import Colours
from colours import NUMBER_OF_COLOURS

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

            pixels[x][y][colour] += 1

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
blended_average = Image.new('RGB', (1000, 1000))
# This is the most common colour
most_common = Image.new('RGB', (1000, 1000))

# This is for pixels that were never placed
never_placed = Image.new('RGB', (1000, 1000))

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

        r = 0
        g = 0
        b = 0
        if total_placed != 0:
            r = int(total_r / total_placed)
            g = int(total_g / total_placed)
            b = int(total_b / total_placed)
        blended_average.putpixel((x, y), (r, g, b))

        if most_num > 0:
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

        else:
            never_placed.putpixel((x, y), (256, 256, 256))

        print_progress(x * 1000 + y, NUM_PIXELS)

print()

blended_average.save('blended_average.png')
most_common.save('most_common.png')
never_placed.save('never_placed.png')
