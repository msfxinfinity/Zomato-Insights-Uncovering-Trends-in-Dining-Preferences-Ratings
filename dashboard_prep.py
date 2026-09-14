"""
Cleans Zomato Data.csv and exports a Tableau-ready CSV with derived fields.

Run this from inside the Zomato-Insights repo (same folder as `Zomato Data.csv`):
    python3 dashboard_prep.py

Writes `zomato_clean.csv` with two new columns Tableau can't reliably derive
on its own without a calculated field first: a numeric rating (the raw
`rate` column is a string like "4.1/5") and a price bracket bucket.
"""
import pandas as pd

df = pd.read_csv("Zomato Data.csv")

# rate looks like "4.1/5" -- some public versions of this dataset also have
# "NEW" or "-" for brand-new/unrated listings, so guard for that even if this
# copy doesn't have any.
def parse_rating(val):
    if not isinstance(val, str) or "/" not in val:
        return None
    try:
        return float(val.split("/")[0])
    except ValueError:
        return None

df["rating_numeric"] = df["rate"].apply(parse_rating)

# approx_cost(for two people) can be read as a string if larger values contain
# commas (e.g. "1,200"); normalize defensively.
cost_col = "approx_cost(for two people)"
df[cost_col] = (
    df[cost_col].astype(str).str.replace(",", "", regex=False).astype(float)
)

def price_bracket(cost):
    if cost <= 300:
        return "Budget (<=Rs300)"
    if cost <= 600:
        return "Mid-range (Rs301-600)"
    if cost <= 1000:
        return "Premium (Rs601-1000)"
    return "Fine Dining (Rs1000+)"

df["price_bracket"] = df[cost_col].apply(price_bracket)

def rating_bucket(r):
    if r is None:
        return "Unrated"
    if r >= 4.5:
        return "4.5+ (Excellent)"
    if r >= 4.0:
        return "4.0-4.49 (Good)"
    if r >= 3.5:
        return "3.5-3.99 (Average)"
    if r >= 3.0:
        return "3.0-3.49 (Below Average)"
    return "Under 3.0"

df["rating_bucket"] = df["rating_numeric"].apply(rating_bucket)

df.to_csv("zomato_clean.csv", index=False)
print("Wrote zomato_clean.csv:", len(df), "rows")
print(df[["name", "rating_numeric", cost_col, "price_bracket", "rating_bucket"]].head())
