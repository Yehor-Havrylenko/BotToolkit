#!/usr/bin/env python3
import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python convert.py input_file.xlsx")
    sys.exit(1)

input_file = sys.argv[1]

try:
    df = pd.read_excel(input_file)
    df.to_csv("output_file.csv", index=False)
    print(f"File Converted")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)