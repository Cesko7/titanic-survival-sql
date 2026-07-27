# Titanic Survival Analysis (SQL)

A beginner-friendly SQL project exploring who survived the 1912 sinking of the
Titanic. The real passenger dataset (891 passengers) is loaded into a small
SQLite database and queried to answer eight questions about survival, using core
SQL fundamentals.

**[See every question, query, and result in RESULTS.md.](RESULTS.md)**

## What the data shows

Survival was far from random. Overall about **38%** of passengers survived, but
the odds depended heavily on class and sex:

- **Class mattered:** First-class passengers survived at **63%**, second class at
  **47%**, and third class at just **24%**.
- **Sex mattered even more:** **74%** of women survived versus only **19%** of
  men, reflecting the "women and children first" evacuation.
- **The two combined:** first-class women survived at **97%**, while third-class
  men survived at **14%**.
- **Fare tracked survival:** passengers who paid more than the average fare
  survived at **60%**, well above the overall rate, since fare is closely tied to
  class.
- **Children** (age 12 and under) survived at **58%**, higher than any adult
  group.

## SQL skills demonstrated

This project sticks to the fundamentals that matter most in day-to-day analyst
work:

- `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT`-style filtering
- Aggregate functions (`COUNT`, `SUM`, `AVG`) with `ROUND`
- `GROUP BY`, including grouping by two columns at once
- `JOIN`s from the passengers table to two small lookup tables (class and port)
- A `CASE` expression to bucket ages into groups
- Handling missing data with `IS NOT NULL`
- A subquery to compare each passenger to the overall average fare

## Database design

One main table with two lookup tables that give readable labels:

```
ticket_class (3 rows)        port (3 rows)
  pclass  PK                   port_code  PK
  class_name                   port_name
        \                          /
         \                        /
             passengers (891 rows)
               passenger_id PK
               survived, sex, age, sibsp, parch, fare
               pclass    -> ticket_class
               embarked  -> port
```

## Repository contents

| Path | Description |
|------|-------------|
| `sql/schema.sql` | Table definitions |
| `sql/queries.sql` | All eight queries |
| `RESULTS.md` | Each question with its query and result |
| `build_db.py` | Builds `titanic.db` from the CSV and schema |
| `run_analysis.py` | Runs the queries and regenerates `RESULTS.md` |
| `data/titanic.csv` | The dataset (891 passengers) |

## Running it yourself

```bash
pip install pandas tabulate
python build_db.py        # creates titanic.db
python run_analysis.py    # runs the queries, rewrites RESULTS.md
```

You can also open `titanic.db` in any SQLite client and run the statements in
`sql/queries.sql` directly.

## Data source

The Titanic passenger dataset, distributed with the seaborn library and widely
used for teaching data analysis.

## License

Released under the [MIT License](LICENSE).
