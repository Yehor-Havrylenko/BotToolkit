#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file.xlsx output_dir"
    exit 1
fi

input_file="$1"
output_dir="$2"

python3 export_xlsx_to_csv.py "$input_file"

output_csv="output_file.csv"

python3 Dialog_Requirements_Generator/main.py "$output_csv" "$output_dir"
cd text_handler/
bash handler_starter.sh "$output_dir" 60
cd ..
rm output_file.csv