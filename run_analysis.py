"""Run each query and write sql/queries.sql + RESULTS.md."""
import sqlite3, pandas as pd

QUERIES = [
("How many passengers survived?",
 "A first look: total passengers, how many survived, and the overall survival rate.",
"""SELECT COUNT(*)                             AS total_passengers,
       SUM(survived)                        AS survivors,
       ROUND(AVG(survived) * 100, 1)        AS survival_rate_pct
FROM passengers;"""),

("Survival rate by passenger class",
 "Join to the class lookup table and group by class to see if ticket class mattered.",
"""SELECT tc.class_name,
       COUNT(*)                        AS passengers,
       SUM(p.survived)                 AS survivors,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY p.pclass;"""),

("Survival rate by sex",
 "Group by sex to compare survival between men and women.",
"""SELECT sex,
       COUNT(*)                        AS passengers,
       SUM(survived)                   AS survivors,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
GROUP BY sex
ORDER BY survival_rate_pct DESC;"""),

("Average fare paid by class",
 "How much did each class pay on average? Round the result for readability.",
"""SELECT tc.class_name,
       COUNT(*)                 AS passengers,
       ROUND(AVG(p.fare), 2)    AS avg_fare
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY avg_fare DESC;"""),

("Survival rate by sex and class",
 "Group by two columns at once to see how sex and class combine.",
"""SELECT tc.class_name,
       p.sex,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.sex, p.pclass
ORDER BY p.pclass, p.sex;"""),

("Where did passengers board?",
 "Join the port lookup and count passengers per port. The two rows with an "
 "unknown port are excluded with a WHERE filter on NULL.",
"""SELECT po.port_name,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN port po ON po.port_code = p.embarked
WHERE p.embarked IS NOT NULL
GROUP BY po.port_name
ORDER BY passengers DESC;"""),

("Survival rate by age group",
 "Use CASE to bucket ages into groups, skipping the 177 passengers with no "
 "recorded age.",
"""SELECT CASE
           WHEN age < 13 THEN '1. Child (0-12)'
           WHEN age < 20 THEN '2. Teen (13-19)'
           WHEN age < 40 THEN '3. Adult (20-39)'
           WHEN age < 60 THEN '4. Middle age (40-59)'
           ELSE               '5. Senior (60+)'
       END                             AS age_group,
       COUNT(*)                        AS passengers,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
WHERE age IS NOT NULL
GROUP BY age_group
ORDER BY age_group;"""),

("Passengers who paid more than the average fare",
 "A subquery computes the overall average fare; the outer query counts how many "
 "passengers paid above it and how they fared.",
"""SELECT COUNT(*)                        AS above_avg_fare_passengers,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
WHERE fare > (SELECT AVG(fare) FROM passengers);"""),
]

con = sqlite3.connect("titanic.db")

with open("sql/queries.sql","w") as f:
    f.write("-- Analytical queries for the Titanic database.\n"
            "-- Run against titanic.db, built by build_db.py.\n\n")
    for i,(title,desc,sql) in enumerate(QUERIES,1):
        f.write(f"-- {i}. {title}\n-- {desc}\n{sql}\n\n")

with open("RESULTS.md","w") as f:
    f.write("# Query Results\n\n")
    f.write("Eight questions about the 891 passengers on the Titanic, each answered "
            "with one SQL query run against `titanic.db`. The queries use core SQL: "
            "`SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, aggregate functions, `JOIN`s "
            "to two lookup tables, a `CASE` expression, and a subquery.\n\n")
    for i,(title,desc,sql) in enumerate(QUERIES,1):
        df = pd.read_sql_query(sql, con)
        f.write(f"## {i}. {title}\n\n{desc}\n\n```sql\n{sql}\n```\n\n")
        f.write(df.to_markdown(index=False)+"\n\n")
        print(f"Q{i} {title}: {df.shape[0]} rows")

con.close()
print("wrote sql/queries.sql and RESULTS.md")
