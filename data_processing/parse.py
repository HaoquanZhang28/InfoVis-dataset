from pathlib import Path

import pandas as pd


COUNTRY_FILE = "country_codes_V202601.csv"
INPUT_PATTERN = "BACI_HS92_Y*_V202601.csv"
OUTPUT_FILE = "top10_trade.csv"
CHUNK_SIZE = 10**6


def build_top10_codes(country_df: pd.DataFrame) -> set[int]:
    iso_to_code = dict(zip(country_df["country_iso3"], country_df["country_code"]))
    top10_iso = ["USA", "CHN", "JPN", "DEU", "IND", "GBR", "FRA", "ITA", "CAN", "KOR"]
    return {iso_to_code[iso] for iso in top10_iso if iso in iso_to_code}


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    country_df = pd.read_csv(base_dir / COUNTRY_FILE)

    top10_codes = build_top10_codes(country_df)
    code_to_name = dict(zip(country_df["country_code"], country_df["country_name"]))

    input_files = sorted(base_dir.glob(INPUT_PATTERN))
    if not input_files:
        raise FileNotFoundError(f"No files matched pattern: {INPUT_PATTERN}")

    output_path = base_dir / OUTPUT_FILE
    if output_path.exists():
        output_path.unlink()

    total_rows = 0
    wrote_header = False

    print("Top10 codes:", sorted(top10_codes))
    print(f"Found {len(input_files)} input files.")

    for input_file in input_files:
        print(f"Processing {input_file.name}...")

        for chunk in pd.read_csv(
            input_file,
            chunksize=CHUNK_SIZE,
            dtype={
                "t": "int16",
                "i": "int16",
                "j": "int16",
                "k": "string",
                "v": "float32",
                "q": "float32",
            },
        ):
            filtered = chunk[
                chunk["i"].isin(top10_codes) & chunk["j"].isin(top10_codes)
            ].copy()

            if filtered.empty:
                continue

            filtered["k"] = filtered["k"].str.zfill(6)
            filtered["exporter_name"] = filtered["i"].map(code_to_name)
            filtered["importer_name"] = filtered["j"].map(code_to_name)

            filtered.to_csv(output_path, mode="a", header=not wrote_header, index=False)
            wrote_header = True
            total_rows += len(filtered)

    print(f"Done, rows: {total_rows}")
    print(f"Saved to: {output_path.name}")


if __name__ == "__main__":
    main()
