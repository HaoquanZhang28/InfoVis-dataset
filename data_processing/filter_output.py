import pandas as pd

def hs2_to_section(hs2):
    if 1 <= hs2 <= 5:
        return "I - Live animals; animal products"
    if 6 <= hs2 <= 14:
        return "II - Vegetable products"
    if hs2 == 15:
        return "III - Animal or vegetable fats and oils"
    if 16 <= hs2 <= 24:
        return "IV - Prepared foodstuffs; beverages; tobacco"
    if 25 <= hs2 <= 27:
        return "V - Mineral products"
    if 28 <= hs2 <= 38:
        return "VI - Products of the chemical or allied industries"
    if 39 <= hs2 <= 40:
        return "VII - Plastics and rubber"
    if 41 <= hs2 <= 43:
        return "VIII - Raw hides and skins; leather; travel goods"
    if 44 <= hs2 <= 46:
        return "IX - Wood and articles of wood"
    if 47 <= hs2 <= 49:
        return "X - Pulp of wood; paper and paperboard"
    if 50 <= hs2 <= 63:
        return "XI - Textiles and textile articles"
    if 64 <= hs2 <= 67:
        return "XII - Footwear; headgear; umbrellas"
    if 68 <= hs2 <= 70:
        return "XIII - Articles of stone, plaster, cement, glass"
    if hs2 == 71:
        return "XIV - Natural or cultured pearls; precious stones"
    if 72 <= hs2 <= 83:
        return "XV - Base metals and articles of base metal"
    if 84 <= hs2 <= 85:
        return "XVI - Machinery and electrical equipment"
    if 86 <= hs2 <= 89:
        return "XVII - Vehicles, aircraft, vessels"
    if 90 <= hs2 <= 92:
        return "XVIII - Optical, medical, measuring instruments"
    if hs2 == 93:
        return "XIX - Arms and ammunition"
    if 94 <= hs2 <= 96:
        return "XX - Miscellaneous manufactured articles"
    if hs2 == 97:
        return "XXI - Works of art, collectors' pieces and antiques"
    return "Unknown"

df = pd.read_csv("top10_trade.csv")
# Make sure product code is always six digits before extracting HS2.
df["k"] = df["k"].astype(str).str.zfill(6)
df["hs2"] = df["k"].str[:2].astype(int)
df["hs_section"] = df["hs2"].apply(hs2_to_section)
# Aggregate rows that share year, exporter, importer, and HS Section.
grouped_df = (
    df.groupby(
        ["t", "i", "j", "exporter_name", "importer_name", "hs_section"],
        as_index=False,
    )
    .agg({"v": "sum", "q": "sum"})
    .sort_values(["t", "i", "j", "hs_section"])
)

grouped_df = grouped_df.rename(
    columns={
        "t": "year",
        "i": "exporter_code",
        "j": "importer_code",
        "v": "value",
        "q": "quantity",
    }
)
# Drop data with zero quantity
grouped_df = grouped_df[grouped_df["quantity"] != 0]
# Filter out data from 2014 and later years
grouped_df = grouped_df[grouped_df["year"] < 2014]
grouped_df.to_csv("top10_trade_final.csv", index=False)
print("Filtered data saved to top10_trade_final.csv")
