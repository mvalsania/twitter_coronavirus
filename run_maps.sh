#!/bin/bash

# Loop over each matching file
for file in '/data/Twitter dataset/'geoTwitter20*; do
    echo "Starting map.py on $file"
    # nohup ensures the process is not killed after disconnection,
    # and & runs the process in the background.
    nohup python3 src/map.py --input_path="$file" &
done
