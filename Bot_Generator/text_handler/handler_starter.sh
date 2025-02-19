#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIRECTORY="$1"

find "$DIRECTORY" -type f -name "*.yaml" | while read -r file; do
    echo "Processing: $file"
    python3 text_handler.py "$file" 60
done

echo "All YAML files processed."
