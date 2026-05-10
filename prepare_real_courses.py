import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_FILE = os.path.join(BASE_DIR, "data_raw", "myskillsfuture_courses.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "courses")


def clean(value):
    if pd.isna(value):
        return "Not stated"
    return str(value).strip()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_excel(RAW_FILE)

    print("Columns found:")
    print(df.columns.tolist())

    for file_no, (_, row) in enumerate(df.iterrows(), start=1):
        content = ""

        for col in df.columns:
            content += f"{col}: {clean(row[col])}\n"

        file_name = f"real_course_{file_no:04d}.txt"

        with open(os.path.join(OUTPUT_DIR, file_name), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Converted {len(df)} courses into txt files.")
    print(f"Saved into: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()