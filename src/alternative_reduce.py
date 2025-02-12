#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True,
                    help="List of hashtags to plot (e.g., --hashtags '#coronavirus' '#covid19')")
args = parser.parse_args()

# Use a non-interactive backend for matplotlib (useful on headless systems)
import matplotlib
matplotlib.use('Agg')

import os
import json
import matplotlib.pyplot as plt

# hashtag_daily_counts will hold, for each hashtag, a dictionary that maps a date (as a string)
# to the tweet count for that day.
hashtag_daily_counts = {}

# Loop over each hashtag provided as input.
for hashtag in args.hashtags:
    daily_counts = {}  # This dictionary will store tweet counts per day for the current hashtag.
    # Loop through all files in the "outputs" directory.
    for output_filename in sorted(os.listdir('outputs')):
        file_path = os.path.join('outputs', output_filename)
        # Extract the date string from the filename.
        # Assumes filename format like: geoTwitterYY-MM-DD.zip.lang where the date is at positions 10:18.
        date_str = output_filename[10:18]
        # Process only if it's a file and if "lang" is in the filename.
        if os.path.isfile(file_path) and 'lang' in output_filename:
            daily_tweet_count = 0
            with open(file_path) as f:
                data = json.load(f)
                if hashtag in data:
                    # Sum tweet counts across all subkeys (e.g., languages) for the hashtag.
                    daily_tweet_count = sum(data[hashtag].values())
            daily_counts[date_str] = daily_tweet_count
    hashtag_daily_counts[hashtag] = daily_counts

# Plotting the results
plt.figure(figsize=(14, 8))
for hashtag, counts_by_date in hashtag_daily_counts.items():
    # Sort the dates so the line plot is ordered.
    sorted_dates = sorted(counts_by_date.keys())
    # Create a list of tweet counts corresponding to the sorted dates.
    tweet_counts = [counts_by_date[date] for date in sorted_dates]
    plt.plot(sorted_dates, tweet_counts, label=hashtag, linewidth=1.5)

plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.title('Tweet Counts by Hashtag(s) Over Time')
plt.legend()

# Optionally, reduce x-tick clutter by selecting a subset of dates.
all_dates = sorted(hashtag_daily_counts[next(iter(hashtag_daily_counts))].keys())
selected_dates = all_dates[::20]  # Show every 20th date.
plt.xticks(selected_dates, rotation=45)

plt.tight_layout()
plt.savefig('hashtag_trends.png')
plt.close()

