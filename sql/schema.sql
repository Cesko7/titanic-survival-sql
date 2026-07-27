-- Schema for the Titanic passenger dataset.
-- The passengers table holds one row per passenger. Two small lookup tables give
-- readable names for the ticket class and the port where each passenger boarded,
-- so queries can JOIN to show "First" instead of 1 and "Cherbourg" instead of C.

DROP TABLE IF EXISTS passengers;
DROP TABLE IF EXISTS ticket_class;
DROP TABLE IF EXISTS port;

CREATE TABLE ticket_class (
    pclass     INTEGER PRIMARY KEY,   -- 1, 2, 3
    class_name TEXT NOT NULL          -- First, Second, Third
);

CREATE TABLE port (
    port_code TEXT PRIMARY KEY,       -- C, Q, S
    port_name TEXT NOT NULL           -- Cherbourg, Queenstown, Southampton
);

CREATE TABLE passengers (
    passenger_id INTEGER PRIMARY KEY,
    survived     INTEGER NOT NULL,    -- 1 = survived, 0 = did not
    pclass       INTEGER NOT NULL REFERENCES ticket_class(pclass),
    sex          TEXT    NOT NULL,
    age          REAL,                -- NULL when unknown
    sibsp        INTEGER,             -- siblings / spouses aboard
    parch        INTEGER,             -- parents / children aboard
    fare         REAL,
    embarked     TEXT REFERENCES port(port_code)   -- NULL for 2 passengers
);
