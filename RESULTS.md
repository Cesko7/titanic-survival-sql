# Query Results

Eight questions about the 891 passengers on the Titanic, each answered with one SQL query run against `titanic.db`. The queries use core SQL: `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, aggregate functions, `JOIN`s to two lookup tables, a `CASE` expression, and a subquery.

## 1. How many passengers survived?

A first look: total passengers, how many survived, and the overall survival rate.

```sql
SELECT COUNT(*)                             AS total_passengers,
       SUM(survived)                        AS survivors,
       ROUND(AVG(survived) * 100, 1)        AS survival_rate_pct
FROM passengers;
```

|   total_passengers |   survivors |   survival_rate_pct |
|-------------------:|------------:|--------------------:|
|                891 |         342 |                38.4 |

## 2. Survival rate by passenger class

Join to the class lookup table and group by class to see if ticket class mattered.

```sql
SELECT tc.class_name,
       COUNT(*)                        AS passengers,
       SUM(p.survived)                 AS survivors,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY p.pclass;
```

| class_name   |   passengers |   survivors |   survival_rate_pct |
|:-------------|-------------:|------------:|--------------------:|
| First        |          216 |         136 |                63   |
| Second       |          184 |          87 |                47.3 |
| Third        |          491 |         119 |                24.2 |

## 3. Survival rate by sex

Group by sex to compare survival between men and women.

```sql
SELECT sex,
       COUNT(*)                        AS passengers,
       SUM(survived)                   AS survivors,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
GROUP BY sex
ORDER BY survival_rate_pct DESC;
```

| sex    |   passengers |   survivors |   survival_rate_pct |
|:-------|-------------:|------------:|--------------------:|
| female |          314 |         233 |                74.2 |
| male   |          577 |         109 |                18.9 |

## 4. Average fare paid by class

How much did each class pay on average? Round the result for readability.

```sql
SELECT tc.class_name,
       COUNT(*)                 AS passengers,
       ROUND(AVG(p.fare), 2)    AS avg_fare
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY avg_fare DESC;
```

| class_name   |   passengers |   avg_fare |
|:-------------|-------------:|-----------:|
| First        |          216 |      84.15 |
| Second       |          184 |      20.66 |
| Third        |          491 |      13.68 |

## 5. Survival rate by sex and class

Group by two columns at once to see how sex and class combine.

```sql
SELECT tc.class_name,
       p.sex,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.sex, p.pclass
ORDER BY p.pclass, p.sex;
```

| class_name   | sex    |   passengers |   survival_rate_pct |
|:-------------|:-------|-------------:|--------------------:|
| First        | female |           94 |                96.8 |
| First        | male   |          122 |                36.9 |
| Second       | female |           76 |                92.1 |
| Second       | male   |          108 |                15.7 |
| Third        | female |          144 |                50   |
| Third        | male   |          347 |                13.5 |

## 6. Where did passengers board?

Join the port lookup and count passengers per port. The two rows with an unknown port are excluded with a WHERE filter on NULL.

```sql
SELECT po.port_name,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN port po ON po.port_code = p.embarked
WHERE p.embarked IS NOT NULL
GROUP BY po.port_name
ORDER BY passengers DESC;
```

| port_name   |   passengers |   survival_rate_pct |
|:------------|-------------:|--------------------:|
| Southampton |          644 |                33.7 |
| Cherbourg   |          168 |                55.4 |
| Queenstown  |           77 |                39   |

## 7. Survival rate by age group

Use CASE to bucket ages into groups, skipping the 177 passengers with no recorded age.

```sql
SELECT CASE
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
ORDER BY age_group;
```

| age_group             |   passengers |   survival_rate_pct |
|:----------------------|-------------:|--------------------:|
| 1. Child (0-12)       |           69 |                58   |
| 2. Teen (13-19)       |           95 |                41.1 |
| 3. Adult (20-39)      |          387 |                38.8 |
| 4. Middle age (40-59) |          137 |                39.4 |
| 5. Senior (60+)       |           26 |                26.9 |

## 8. Passengers who paid more than the average fare

A subquery computes the overall average fare; the outer query counts how many passengers paid above it and how they fared.

```sql
SELECT COUNT(*)                        AS above_avg_fare_passengers,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
WHERE fare > (SELECT AVG(fare) FROM passengers);
```

|   above_avg_fare_passengers |   survival_rate_pct |
|----------------------------:|--------------------:|
|                         211 |                59.7 |

