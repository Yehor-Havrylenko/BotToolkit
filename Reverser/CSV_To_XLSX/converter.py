#!/usr/bin/env python3
import pandas as pd
import sys

def csv_to_xlsx(csv_file, xlsx_file):
    df = pd.read_csv(csv_file, delimiter=",", encoding="utf-8")
    df.to_excel(xlsx_file, index=False, engine="openpyxl")
    print(f"XLSX created: {xlsx_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python csv_to_xlsx.py input.csv output.xlsx")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    xlsx_file = sys.argv[2]
    
    csv_to_xlsx(csv_file, xlsx_file)
