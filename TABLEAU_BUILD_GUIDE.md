# Tableau Build Guide -- Zomato Restaurant Performance Dashboard

Extends the existing pandas/EDA analysis in this repo with an interactive
Tableau Public dashboard. Run `dashboard_prep.py` first (needs `Zomato
Data.csv` in the same folder — it's already in this repo) to produce
`zomato_clean.csv`, then build the dashboard against that file.

```bash
python3 dashboard_prep.py
```

## 0. Connect

Tableau Public → **Connect → Text File** → `zomato_clean.csv`.

Columns you'll use (from the real file): `name`, `online_order`, `book_table`,
`rate`, `votes`, `approx_cost(for two people)`, `listed_in(type)`, plus the
derived `rating_numeric`, `price_bracket`, `rating_bucket` columns
`dashboard_prep.py` adds.

## 1. Parameter (interactivity requirement)

Create Parameter:
- Name: `Minimum Votes`
- Data type: Integer
- Range: 0 to 3000, step 50
- Default: 50

(This models a real analyst decision: restaurants with very few votes have
unreliable ratings, so letting the viewer raise the threshold is a
legitimate filter, not decoration.)

## 2. Calculated field

**`Meets Vote Threshold`**
```
[votes] >= [Minimum Votes]
```
Right-click `Minimum Votes` → **Show Parameter Control**.

## 3. Sheet 1 — Cost vs Rating

- Columns: `approx_cost(for two people)` (continuous).
- Rows: `rating_numeric` (continuous, Average).
- Detail: `name`.
- Color: `listed_in(type)`.
- Size: `votes` (Sum).
- Mark type: **Circle**.
- Filters shelf: drag `Meets Vote Threshold` → keep only **True**.
- Rename sheet: `Cost vs Rating`.

## 4. Sheet 2 — Online Ordering by Price Bracket

Create calculated field **`Online Order Rate`**:
```
SUM(IF [online_order] = "Yes" THEN 1 ELSE 0 END) / COUNT([online_order])
```
- Columns: `price_bracket`.
- Rows: `Online Order Rate`. Format axis as percentage.
- Filters shelf: drag `Meets Vote Threshold` → keep only **True**.
- Mark type: **Bar**.
- Rename sheet: `Online Ordering by Price Bracket`.

## 5. Sheet 3 — Restaurant Type Breakdown

- Columns: `listed_in(type)`.
- Rows: `COUNTD(name)`.
- Color: `AVG(rating_numeric)` (use a diverging or sequential palette so type
  and average rating are both visible at a glance).
- Mark type: **Bar**.
- Rename sheet: `Restaurant Type Breakdown`.

## 6. Dashboard + filter action

New Dashboard → add all three sheets (`Cost vs Rating` on top,
`Online Ordering by Price Bracket` and `Restaurant Type Breakdown` side by
side below).

Dashboard → Actions → Add Action → **Filter**
- Source sheet: `Restaurant Type Breakdown`
- Target sheets: `Cost vs Rating`, `Online Ordering by Price Bracket`
- Run action on: **Select**
- Clearing the selection: **Show all values**

Result: clicking a restaurant type (e.g. "Cafes") in the breakdown chart
filters the scatter plot and the online-ordering chart down to just that
type.

## 7. Publish

File → **Save to Tableau Public As...** → name it
`Zomato Restaurant Performance Dashboard`. Copy the published URL.

## 8. After publishing

Send me the URL and I'll add it to the Data Analyst resume's Zomato project
entry, and add a screenshot + link to this repo's README.
