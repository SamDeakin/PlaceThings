COLOUR_NUMBERS := 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

NEVER_PLACED_DIR := results/never-placed
NEVER_PLACED_FILES := $(addprefix $(NEVER_PLACED_DIR)/, never-placed.png never-placed-light.png never-placed-dark.png)

HEATMAPS_DIR := results/heatmaps
HEATMAPS_FILES := $(addprefix $(HEATMAPS_DIR)/, heatmap-total.png heatmap-total-dark.png heatmap-total-light.png $(foreach number, $(COLOUR_NUMBERS), heatmap-$(number).png heatmap-$(number)-dark.png heatmap-$(number)-light.png))

BLENDED_AVERAGE := results/blended-average.png
MOST_COMMON := results/most-common.png

all: $(NEVER_PLACED_FILES) $(HEATMAPS_FILES) $(BLENDED_AVERAGE) $(MOST_COMMON)

sorted.csv: tile_placements.csv
	sort -o sorted.csv tile_placements.csv

frequencies.csv:
	python3 frequencies.py

$(NEVER_PLACED_DIR):
	mkdir $(NEVER_PLACED_DIR)

$(NEVER_PLACED_DIR)/%.png: never_placed.py frequencies.csv | $(NEVER_PLACED_DIR)
	python3 never_placed.py

$(HEATMAPS_DIR):
	mkdir $(HEATMAPS_DIR)

$(HEATMAPS_DIR)/%.png: heatmaps.py frequencies.csv | $(HEATMAPS_DIR)
	pyton3 heatmaps.py

$(BLENDED_AVERAGE): blended_average.py frequencies.csv
	python3 blended_average.py

$(MOST_COMMON): most_common.py frequencies.csv
	python3 most_common.py

.PHONY: clean
clean:
	rm sorted.csv
	rm frequencies.csv
	rm -rf $(NEVER_PLACED_DIR)
	rm -rf $(HEATMAPS_DIR)
	rm results/*.png
