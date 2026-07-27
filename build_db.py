"""Build titanic.db: create the schema and load data/titanic.csv."""
import sqlite3, pandas as pd

df = pd.read_csv("data/titanic.csv")

con = sqlite3.connect("titanic.db")
with open("sql/schema.sql") as f:
    con.executescript(f.read())
cur = con.cursor()

cur.executemany("INSERT INTO ticket_class VALUES (?,?)",
                [(1,"First"),(2,"Second"),(3,"Third")])
cur.executemany("INSERT INTO port VALUES (?,?)",
                [("C","Cherbourg"),("Q","Queenstown"),("S","Southampton")])

rows = [(int(r.passenger_id), int(r.survived), int(r.pclass), r.sex,
         None if pd.isna(r.age) else float(r.age),
         None if pd.isna(r.sibsp) else int(r.sibsp),
         None if pd.isna(r.parch) else int(r.parch),
         None if pd.isna(r.fare) else float(r.fare),
         None if pd.isna(r.embarked) else r.embarked)
        for r in df.itertuples(index=False)]
cur.executemany("INSERT INTO passengers VALUES (?,?,?,?,?,?,?,?,?)", rows)
con.commit()

print("passengers loaded:", cur.execute("SELECT COUNT(*) FROM passengers").fetchone()[0])
con.close()
