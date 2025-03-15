#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file.xlsx output_dir"
    exit 1
fi

input_file="$1"
output_dir="$2"
script_dir="$(cd "$(dirname "$0")" && pwd)"
output_csv="$script_dir/TemporaryData/converted.csv"

mkdir -p "$script_dir/TemporaryData/"

extension="${input_file##*.}"
if [ "$extension" == "xlsx" ]; then
    python3 "$script_dir/Reverser/XLSX_To_CSV/converter.py" "$input_file" "$output_csv"
elif [ "$extension" == "csv" ]; then
    output_csv="$input_file"
else
    echo "Error: Unsupported file format. Please provide an XLSX or CSV file."
    exit 1
fi

if [ ! -f "$output_csv" ]; then
    echo "Error: CSV conversion failed, file not found: $output_csv"
    exit 1
fi

python3 "$script_dir/Bot_Generator/Dialog_Requirements_Generator/main.py" "$output_csv" "$output_dir"

bash "$script_dir/Bot_Generator/text_handler/handler_starter.sh" "$output_dir"
rm -rf "$script_dir/TemporaryData/"
