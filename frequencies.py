# python3
import traceback

from colours import NUMBER_OF_COLOURS
from utils import print_progress

print('Setting up...')

# The number of lines in tile_placements.csv
# This is hardcoded because there's no way to get it without reading the entire file
# and it will only be used for the progress bar
NUM_LINES = 16559898
NUM_PIXELS = 1000 * 1000

pixels = [[[0 for i in range(NUMBER_OF_COLOURS)] for j in range(1000)] for k in range(1000)]

# (timestamp, colour)
final_pixel = [[(0, 0) for i in range(1000)] for k in range(1000)]

# (total, highest)
total = [0 for i in range(NUMBER_OF_COLOURS)]
highest = [0 for i in range(NUMBER_OF_COLOURS)]

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

            colour_count = pixels[x][y][colour] + 1
            pixels[x][y][colour] = colour_count
            total[colour] += 1
            if highest[colour] < colour_count:
                highest[colour] = colour_count

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

print('Writing to file...')

# Now we print out what we've calculated
with open('frequencies.csv', 'w') as f:
    def writeline(*args):
        f.write(','.join(map(str, args)) + '\n')

    # The first line is the column names
    f.write('x,y,Colour 0,Colour 1,Colour 2,Colour 3,Colour 4,Colour 5,Colour 6,Colour 7,Colour 8,Colour 9,Colour 10,Colour 11,Colour 12,Colour 13,Colour 14,Colour 15,Final Colour\n')

    # The next two lines written are totals
    # Line 1 is the total for each colour
    writeline(-1, -1, *total, sum(*total))

    # Line 2 is the highest of each colour
    writeline(-1, -1, *highest, max(*highest))

    for x in range(1000):
        for y in range(1000):
            writeline(x, y, *pixels[x][y], final_pixel[x][y][1])
            print_progress(x * 1000 + y, NUM_PIXELS)

print()
