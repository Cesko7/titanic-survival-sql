-- Analytical queries for the Titanic database.
-- Run against titanic.db, built by build_db.py.

-- 1. How many passengers survived?
-- A first look: total passengers, how many survived, and the overall survival rate.
SELECT COUNT(*)                             AS total_passengers,
       SUM(survived)                        AS survivors,
       ROUND(AVG(survived) * 100, 1)        AS survival_rate_pct
FROM passengers;

-- 2. Survival rate by passenger class
-- Join to the class lookup table and group by class to see if ticket class mattered.
SELECT tc.class_name,
       COUNT(*)                        AS passengers,
       SUM(p.survived)                 AS survivors,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY p.pclass;

-- 3. Survival rate by sex
-- Group by sex to compare survival between men and women.
SELECT sex,
       COUNT(*)                        AS passengers,
       SUM(survived)                   AS survivors,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
GROUP BY sex
ORDER BY survival_rate_pct DESC;

-- 4. Average fare paid by class
-- How much did each class pay on average? Round the result for readability.
SELECT tc.class_name,
       COUNT(*)                 AS passengers,
       ROUND(AVG(p.fare), 2)    AS avg_fare
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.pclass
ORDER BY avg_fare DESC;

-- 5. Survival rate by sex and class
-- Group by two columns at once to see how sex and class combine.
SELECT tc.class_name,
       p.sex,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN ticket_class tc ON tc.pclass = p.pclass
GROUP BY tc.class_name, p.sex, p.pclass
ORDER BY p.pclass, p.sex;

-- 6. Where did passengers board?
-- Join the port lookup and count passengers per port. The two rows with an unknown port are excluded with a WHERE filter on NULL.
SELECT po.port_name,
       COUNT(*)                        AS passengers,
       ROUND(AVG(p.survived) * 100, 1) AS survival_rate_pct
FROM passengers p
JOIN port po ON po.port_code = p.embarked
WHERE p.embarked IS NOT NULL
GROUP BY po.port_name
ORDER BY passengers DESC;

-- 7. Survival rate by age group
-- Use CASE to bucket ages into groups, skipping the 177 passengers with no recorded age.
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

-- 8. Passengers who paid more than the average fare
-- A subquery computes the overall average fare; the outer query counts how many passengers paid above it and how they fared.
SELECT COUNT(*)                        AS above_avg_fare_passengers,
       ROUND(AVG(survived) * 100, 1)   AS survival_rate_pct
FROM passengers
WHERE fare > (SELECT AVG(fare) FROM passengers);

