#!/bin/bash

# Check if the input file is provided
if [ $# -ne 2 ]; then
    exit 1
fi

input_file="$1"
output_file="$2"

convert "$input_file" -resize 2000x2000\> "$output_file"
