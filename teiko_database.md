# Problem 1

```sql
CREATE TABLE  samples (
    sample_id INTEGER PRIMARY KEY,
    sample_type VARCHAR(50),
    time_from_treatment_start DECIMAL(10, 2)
);

CREATE TABLE subjects (
    subject_id VARCHAR(30) PRIMARY KEY,
    condition VARCHAR(50),
    sample_id INTEGER,
    age INTEGER,
    sex VARCHAR(10) NOT NULL,
    treatment VARCHAR(50) NOT NULL,
    response VARCHAR(10),
    project VARCHAR(10) NOT NULL,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

-- It makes the most sense to me to create a cells table so that the 
-- data can be stored efficiently, even if different cell types are recorded/found
CREATE TABLE cells (
    cell_id INTEGER PRIMARY KEY,
    sample_id INTEGER,
    cell_type VARCHAR(50) NOT NULL,
    count INTEGER,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);
```

# Problem 2
Capturing this type of data in a database has several advantages.

1. Accessibility: With all of this data in a Database, it would be easy for various researchers/statisticians to access all of the data
2. Consistency: With a DBMS, then the data will remain consistent and neccessary information will not be lost or confused
3. Security: Authentication would be required to access the database, making the data more secure
4. Data Analysis: Many databases are easy to integrate with standard data analysis tools like python and R which makes analyzing the data easier and more accessible

# Problem 3

```sql

SELECT 
condition
, COUNT(DISTINCT subject_id) AS count_subjects
FROM subjects
GROUP BY condition;
```

# Problem 4

```sql

SELECT *
FROM subjects
LEFT JOIN samples
    ON subjects.sample_id = samples.sample_id
WHERE subjects.condition = 'melanoma'
    AND samples.sample_type = 'PBMC'
    AND samples.time_from_treatment_start = 0
    AND subjects.treatment = 'tr1';

```

# Problem 5
## a.
```sql

SELECT 
subjects.project
, count(DISTINCT subjects.sample_id) AS count
FROM subjects
LEFT JOIN samples
    ON subjects.sample_id = samples.sample_id
WHERE subjects.condition = 'melanoma'
    AND samples.sample_type = 'PBMC'
    AND samples.time_from_treatment_start = 0
    AND subjects.treatment = 'tr1'
GROUP BY subjects.project;
```

## b.

```sql

WITH subset AS(
    SELECT *
    FROM subjects
    LEFT JOIN samples
        ON subjects.sample_id = samples.sample_id
    WHERE subjects.condition = 'melanoma'
        AND samples.sample_type = 'PBMC'
        AND samples.time_from_treatment_start = 0
        AND subjects.treatment = 'tr1'
)

SELECT 
response
, COUNT(DISTINCT subject_id) AS count
FROM subset
GROUP BY response;
```

## c.
```sql
WITH subset AS(
    SELECT *
    FROM subjects
    LEFT JOIN samples
        ON subjects.sample_id = samples.sample_id
    WHERE subjects.condition = 'melanoma'
        AND samples.sample_type = 'PBMC'
        AND samples.time_from_treatment_start = 0
        AND subjects.treatment = 'tr1'
)

SELECT 
sex
, COUNT(DISTINCT subject_id) AS count
FROM subset
GROUP BY sex;
```
