import pandas as pd
import sqlite3 as sq

df = pd.read_csv("Traffic_CrashesData.csv")

#print(df.head())

#print(df.tail())

#print(df.shape)

conn = sq.connect('Crash_Project.db')

df.to_sql('traffic_crashesdata', conn, if_exists='replace', index=False)

TABLE_NAME = "traffic_crashesdata"
TOP_1 = 1
TOP_3 = 3
TOP_5 = 5
TOP_10 = 10
#checking row count
query_rows = """
SELECT COUNT(*) as row_count FROM traffic_crashesdata;
"""
print(pd.read_sql(query_rows, conn))


query_dtypes = """
PRAGMA table_info(traffic_crashesdata);
"""
print(pd.read_sql(query_dtypes, conn))

#1. top 5 most dangerous combinations of weather and crash type based on total crashes
query_weather = f"""SELECT
    WEATHER_CONDITION, CRASH_TYPE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
FROM
    {TABLE_NAME}
  GROUP BY WEATHER_CONDITION , CRASH_TYPE
  ORDER BY TOTAL_CRASHES DESC
LIMIT 5;
"""

print(("\n\ntop 5 most dangerous combinations of weather and crash type based on total crashes\n\n").upper(), pd.read_sql(query_weather, conn))

#2. top 10 streets with the highest number of injury crashes.
query_streets = f"""SELECT
    STREET_NAME, COUNT(CRASH_RECORD_ID) AS INJURY_CRASHES
FROM
    {TABLE_NAME}
  GROUP BY STREET_NAME
  ORDER BY INJURY_CRASHES DESC
LIMIT {TOP_10};
"""

print(("\n\ntop 10 streets with the highest number of injury crashes\n\n").upper(), pd.read_sql(query_streets, conn))

#3. percentage of crashes that resulted in injuries for each crash type.
query_crash_type = f"""SELECT
    FIRST_CRASH_TYPE,
    CRASH_TYPE,
    SUM(INJURIES_TOTAL > 0)*100/COUNT(CRASH_RECORD_ID) AS INJURY_PERCENTAGE
FROM
    {TABLE_NAME}
GROUP BY FIRST_CRASH_TYPE , CRASH_TYPE
HAVING INJURY_PERCENTAGE >0
ORDER BY INJURY_PERCENTAGE DESC
"""
print(("\n\npercentage of crashes that resulted in injuries for each crash type\n\n").upper(), pd.read_sql(query_crash_type, conn))

#4. peak crash hour for each month.
query_peak_hour = f"""
with MONTHLY_CRASHES as
(SELECT CRASH_MONTH, CRASH_HOUR, COUNT(CRASH_RECORD_ID) as CRASH_TOTAL,
RANK() OVER(PARTITION BY CRASH_MONTH ORDER BY COUNT(CRASH_RECORD_ID) DESC) AS CRASH_RANKING
FROM {TABLE_NAME}
GROUP BY CRASH_MONTH, CRASH_HOUR
)

SELECT CRASH_MONTH, CRASH_HOUR, CRASH_TOTAL, CRASH_RANKING
FROM MONTHLY_CRASHES
WHERE CRASH_RANKING = 1;
"""
print(("\n\npeak crash hour for each month\n\n").upper(), pd.read_sql(query_peak_hour, conn))

#5. top 5 primary causes of crashes during nighttime
query_night_time = f"""
SELECT
    PRIM_CONTRIBUTORY_CAUSE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
FROM
    {TABLE_NAME}
WHERE
    CRASH_HOUR >= 18
GROUP BY PRIM_CONTRIBUTORY_CAUSE
ORDER BY total_crashes DESC
LIMIT {TOP_5};
"""
print(("\n\ntop 5 primary causes of crashes during nighttime\n\n").upper(), pd.read_sql(query_night_time, conn))

#6. average number of injuries in daylight vs darkness conditions
query_lightning = f"""
SELECT
    LIGHTING_CONDITION, AVG(INJURIES_TOTAL) AS AVG_INJURY
FROM
    {TABLE_NAME}
WHERE
    LIGHTING_CONDITION IN ('DAYLIGHT' , 'DARKNESS')
GROUP BY LIGHTING_CONDITION;
"""
print(("\n\naverage number of injuries in daylight vs darkness conditions\n\n").upper(), pd.read_sql(query_lightning, conn))

#7. traffic control device type has the highest average injuries per crash
query_traffic_control = f"""
SELECT
    TRAFFIC_CONTROL_DEVICE,
    ROUND(AVG(INJURIES_TOTAL), 3) AS AVG_INJURIES
FROM
    {TABLE_NAME}
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY Avg_injuries DESC;
"""
print(("\n\ntraffic control device type has the highest average injuries per crash\n\n").upper(), pd.read_sql(query_traffic_control, conn))

#8. top 5 locations (latitude/longitude) with the highest crash frequency.
query_location = f"""
SELECT
    LATITUDE, LONGITUDE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
FROM
    {TABLE_NAME}
GROUP BY LATITUDE , LONGITUDE
ORDER BY TOTAL_CRASHES DESC
LIMIT {TOP_5};
"""
print(("\n\ntop 5 locations (latitude/longitude) with the highest crash frequency\n\n").upper(), pd.read_sql(query_location, conn))

#9. top 5 streets with the highest injury rate
query_injury_rate_street = f"""
SELECT
    STREET_NAME, COUNT(INJURIES_TOTAL > 0)*100/count(CRASH_RECORD_ID) as INJURY_RATE,
    COUNT(CRASH_RECORD_ID) as total_crashes

FROM
    {TABLE_NAME}

GROUP BY STREET_NAME
HAVING COUNT(CRASH_RECORD_ID) > 100
ORDER BY total_crashes DESC
LIMIT {TOP_10};
"""
print(("\n\ntop 5 streets with the highest injury rate\n\n").upper(), pd.read_sql(query_injury_rate_street, conn))

#10. most common crash type by year
query_crash_by_year = f"""
SELECT year, FIRST_CRASH_TYPE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES,
RANK() OVER(PARTITION BY year ORDER BY COUNT(CRASH_RECORD_ID) DESC) AS RANKS
FROM {TABLE_NAME}
GROUP BY year, FIRST_CRASH_TYPE;
"""
print(("\n\nmost common crash type by year\n\n").upper(), pd.read_sql(query_crash_by_year, conn))

#11. day of the week with the highest average crashes per hour
query_day_week = f"""
SELECT CRASH_DAY_OF_WEEK, AVG(CRASH_HOUR) AS AVG_CRASH_HOUR
FROM {TABLE_NAME}
GROUP BY CRASH_DAY_OF_WEEK
ORDER BY AVG_CRASH_HOUR DESC;
"""
print(("\n\nday of the week with the highest average crashes per hour\n\n").upper(), pd.read_sql(query_day_week, conn))

#12. Identifying high-risk time slots
query_high_risk_time = f"""
SELECT
CASE WHEN CRASH_HOUR BETWEEN 6 AND 11 THEN 'MORNING'
WHEN CRASH_HOUR BETWEEN 12 AND 16 THEN 'NOON'
WHEN CRASH_HOUR BETWEEN 17 AND 19 THEN 'EVENING'
ELSE 'NIGHT'
END AS TIME_SLOT,
COUNT(CRASH_RECORD_ID) AS TOTAL_INJURY_CRASHES
FROM {TABLE_NAME}
Where INJURIES_TOTAL > 0
GROUP BY TIME_SLOT
ORDER BY TOTAL_INJURY_CRASHES DESC;
"""
print(("\n\nIdentifying high-risk time slots\n\n").upper(), pd.read_sql(query_high_risk_time, conn))

#13. top 3 contributing causes for each crash type
query_contributing_cause = f"""
WITH CAUSE_RANK as (
SELECT
    FIRST_CRASH_TYPE,
    PRIM_CONTRIBUTORY_CAUSE,
    COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES,
    ROW_NUMBER() OVER(PARTITION BY FIRST_CRASH_TYPE ORDER BY COUNT(CRASH_RECORD_ID) DESC) AS RANKS
FROM
    {TABLE_NAME}
GROUP BY FIRST_CRASH_TYPE , PRIM_CONTRIBUTORY_CAUSE
ORDER BY TOTAL_CRASHES DESC
)
SELECT
    FIRST_CRASH_TYPE,
    PRIM_CONTRIBUTORY_CAUSE,
    TOTAL_CRASHES
FROM
    CAUSE_RANK
WHERE
    RANKS <= 3
    LIMIT {TOP_3};
"""
print(("\n\ntop 3 contributing causes for each crash type\n\n").upper(),pd.read_sql(query_contributing_cause, conn))

#14. year-over-year growth rate of crashes
query_year_growth = f"""
SELECT year,
COUNT(CRASH_RECORD_ID) AS total_crashes,
ROUND
    ((COUNT(CRASH_RECORD_ID) - LAG(COUNT(CRASH_RECORD_ID)) OVER(ORDER BY year))
        * 100.0
        /
LAG(COUNT(CRASH_RECORD_ID))
        OVER(ORDER BY year),2) AS percentage_growth

FROM {TABLE_NAME}
GROUP BY year;
"""
print(("\n\nyear-over-year growth rate of crashes\n\n").upper(), pd.read_sql(query_year_growth, conn))

#15. top 10 zone, grouping by locations
query_zones = f"""
SELECT ROUND(LATITUDE, 2) as R_LATITUDE, ROUND(LONGITUDE,2) as R_LONGITUDE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
FROM {TABLE_NAME}
GROUP BY R_LATITUDE, R_LONGITUDE
ORDER BY TOTAL_CRASHES DESC
LIMIT {TOP_10};
"""
print(("\n\ntop 10 zone, grouping by locations\n\n").upper(), pd.read_sql(query_zones, conn))



