#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# Obtain the top 10 keys:
# Sort all key-value pairs (items) in ascending order by value,
# then slice the last 10 items which are the highest counts and are already in ascending order.
sorted_items = sorted(counts[args.key].items(), key=lambda item: item[1])[-10:]

# Extract keys and values for plotting.
keys = [k for k, v in sorted_items]
values = [v for k, v in sorted_items]

# (Optional) print the values for debugging.
for k, v in sorted_items:
    print(f"{k} : {v}")

# Create a bar graph using matplotlib.
plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.ylabel('Percentage' if args.percent else 'Count')
plt.xlabel("Language" if "lang" in args.input_path.lower() else "Country")
plt.title(f"Twitter count for {args.key} by {'Language' if 'lang' in args.input_path.lower() else 'Country'}")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Construct the output image file name.
# For example, if the input is "aggregated.country.json" and key is "#coronavirus",
# the output image will be "aggregated.country_#coronavirus.png"
output_image = os.path.splitext(args.input_path)[0] + "_" + args.key + ".png"

# Save the figure as a PNG file.
plt.savefig(output_image)
plt.close()
