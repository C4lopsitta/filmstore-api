#!/bin/bash

# Check if the input file is provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <image_file> <output_file>"
    exit 1
fi

input_file="$1"
output_file="$2"

# Use ImageMagick's convert command to resize the image
convert "$input_file" -resize 2000x2000\> "$output_file"

echo "Image resized and saved as $output_file"