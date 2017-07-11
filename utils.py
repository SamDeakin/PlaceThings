# python3
import traceback

def print_progress(num, total):
    percent = num / total
    columns = 50
    bar = '#' * int((columns - 2) * percent) + '-' * int((columns - 2) * (1 - percent))
    print('[{bar}] {percent:.2f}%'.format(bar=bar, percent=percent * 100), end='\r')

def load_frequency():
    try:
        with open('frequencies.csv') as f:

            # Skip the first line of column names
            line = f.readline()
            line_num = 1

            # Now read the rest of the lines
            for line_num, line in enumerate(f, 4):
                x, y, *colour_data, overall = line.split(sep=',')
                x = int(x)
                y = int(y)
                pixels = list(map(int, colour_data))
                pixel_total = int(overall)

                yield x, y, pixels, pixel_total

    except:
        traceback.print_exc()
        print('Error at line {num}: "{line}"'.format(num=line_num, line=line.strip()))
        exit(line_num)


