import sqlite3 as sq
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



conn = sq.connect("Crash_Project.db")
st.title("\nTraffic Crash Analysis Dashboard\n")
TABLE_NAME = "traffic_crashesdata"
TOP_1 = 1
TOP_3 = 3
TOP_5 = 5
TOP_10 = 10
case_study = st.selectbox("Select Analysis".upper(),
                          ["SELECT ANY ANALYSIS TO CONTINUE",
                           "1. Top 5 most dangerous combinations of weather and crash type".upper(),
                           "2. top 10 streets with the highest number of injury crashes".upper(),
                           "3. percentage of crashes that resulted in injuries for each crash type".upper(),
                           "4. peak crash hour for each month".upper(),
                           "5. top 5 primary causes of crashes during nighttime".upper(),
                           "6. average number of injuries in daylight vs darkness conditions".upper(),
                           "7. traffic control device type has the highest average injuries per crash".upper(),
                           "8. top 5 locations (latitude/longitude) with the highest crash frequency".upper(),
                           "9. top 5 streets with the highest injury rate".upper(),
                           "10. most common crash type by year".upper(),
                           "11. day of the week with the highest average crashes per hour".upper(),
                           "12. Identifying high-risk time slots".upper(),
                           "13. top 3 contributing causes for each crash type".upper(),
                           "14. year over year growth rate of crashes".upper(),
                           "15. top 10 zone, grouped by locations".upper(),
                           ])

if case_study == "SELECT ANY ANALYSIS TO CONTINUE":
    st.image(r"E:\SQL\Traffic_Project\my_bg.jpg")
    st.markdown("<h4 style='text-align: right;'>by Ahamed N</h4>", unsafe_allow_html=True)

elif case_study == "1. Top 5 most dangerous combinations of weather and crash type".upper():

    query_weather = f"""SELECT
        WEATHER_CONDITION, CRASH_TYPE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
    FROM
        {TABLE_NAME}
      GROUP BY WEATHER_CONDITION , CRASH_TYPE
      ORDER BY TOTAL_CRASHES DESC
    LIMIT {TOP_5};
    """
    df = pd.read_sql(query_weather, conn)
    st.subheader("top 5 dangerous weather:".upper())
    st.dataframe(df)
    st.write("Adverse weather conditions significantly increase the likelihood of specific crash types, indicating environmental impact on road safety risk.")

elif case_study == "2. top 10 streets with the highest number of injury crashes".upper():
    query_streets = f"""SELECT
        STREET_NAME, COUNT(CRASH_RECORD_ID) AS INJURY_CRASHES
    FROM
        {TABLE_NAME}
      GROUP BY STREET_NAME
      ORDER BY INJURY_CRASHES DESC
    LIMIT {TOP_10};
    """
    df = pd.read_sql(query_streets, conn)
    st.subheader("top 10 street with highest injuries:".upper())
    st.dataframe(df)
    st.write("Certain streets consistently show higher injury crash rates, suggesting traffic density and road design as key risk contributors.")

elif case_study == "3. percentage of crashes that resulted in injuries for each crash type".upper():
    query_crash_type = f"""SELECT
        FIRST_CRASH_TYPE,
        CRASH_TYPE,
        SUM(INJURIES_TOTAL > 0)*100/COUNT(CRASH_RECORD_ID) AS INJURY_PERCENTAGE
    FROM
        {TABLE_NAME}
    GROUP BY FIRST_CRASH_TYPE , CRASH_TYPE
    HAVING INJURY_PERCENTAGE >0
    ORDER BY INJURY_PERCENTAGE DESC
    LIMIT {TOP_10};
    """
    df = pd.read_sql(query_crash_type, conn)
    st.subheader("Crashes that resulted in injuries (%):".upper())
    st.dataframe(df)
    st.write("Injury proportions vary across crash types, helping identify which types are more severe and require targeted safety measures.")
    df_sorted = df.sort_values("INJURY_PERCENTAGE", ascending=False)

    plt.figure(figsize=(8, 5))

    plt.bar(df_sorted["FIRST_CRASH_TYPE"], df_sorted["INJURY_PERCENTAGE"])
    plt.xticks(rotation=90)
    st.pyplot(plt)

elif case_study == "4. peak crash hour for each month".upper():
    query_peak_hour = f"""
    with MONTHLY_CRASHES as
    (SELECT CRASH_MONTH, CRASH_HOUR, COUNT(CRASH_RECORD_ID) as CRASH_TOTAL,
    RANK() OVER(PARTITION BY CRASH_MONTH ORDER BY COUNT(CRASH_RECORD_ID) DESC) AS CRASH_RANKING
    FROM {TABLE_NAME}
    GROUP BY CRASH_MONTH, CRASH_HOUR
    )

    SELECT CRASH_MONTH, CRASH_HOUR, CRASH_TOTAL
    FROM MONTHLY_CRASHES
    WHERE CRASH_RANKING = 1;
    """

    df = pd.read_sql(query_peak_hour, conn)
    st.subheader("peak crash hour by month:".upper())
    st.dataframe(df)
    st.write("Crash occurrences peak at specific hours each month, revealing recurring temporal risk patterns tied to daily traffic behavior.")

elif case_study == "5. top 5 primary causes of crashes during nighttime".upper():
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

    df = pd.read_sql(query_night_time, conn)
    st.subheader("Top 5 primary causes:".upper())
    st.dataframe(df)
    st.write("Nighttime crashes are strongly influenced by specific contributing factors, highlighting visibility and driving conditions as major risks.")

elif case_study == "6. average number of injuries in daylight vs darkness conditions".upper():
    query_lightning = f"""
    SELECT
        LIGHTING_CONDITION, AVG(INJURIES_TOTAL) AS AVG_INJURY
    FROM
        {TABLE_NAME}
    WHERE
        LIGHTING_CONDITION IN ('DAYLIGHT' , 'DARKNESS')
    GROUP BY LIGHTING_CONDITION;
    """
    df= pd.read_sql(query_lightning, conn)
    st.subheader("average number of injuries || daylight vs darkness:".upper())
    st.dataframe(df)
    st.write("Injury severity differs between daylight and nighttime, showing that reduced visibility significantly impacts crash outcomes.")

elif case_study == "7. traffic control device type has the highest average injuries per crash".upper():
    query_traffic_control = f"""
    SELECT
        TRAFFIC_CONTROL_DEVICE,
        ROUND(AVG(INJURIES_TOTAL), 3) AS AVG_INJURIES
    FROM
        {TABLE_NAME}
    GROUP BY TRAFFIC_CONTROL_DEVICE
    ORDER BY Avg_injuries DESC;
    """
    df = pd.read_sql(query_traffic_control, conn)
    st.subheader("highest average injuries per crash by traffic control device type:".upper())
    st.dataframe(df)
    st.write("Some traffic control systems are associated with higher injury severity, indicating potential inefficiencies in road regulation systems.")
    st.bar_chart(df.set_index("TRAFFIC_CONTROL_DEVICE")["AVG_INJURIES"])

elif case_study == "8. top 5 locations (latitude/longitude) with the highest crash frequency".upper():
    query_location = f"""
    SELECT
        LATITUDE, LONGITUDE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
    FROM
        {TABLE_NAME}
    GROUP BY LATITUDE , LONGITUDE
    ORDER BY TOTAL_CRASHES DESC
    LIMIT {TOP_5};
    """
    df= pd.read_sql(query_location, conn)
    st.subheader("top 5 locations with highest crash frequency:".upper())
    st.dataframe(df)
    st.write("Crash clustering by location reveals clear geographic hotspots, identifying high-risk zones requiring focused intervention.")

elif case_study == "9. top 5 streets with the highest injury rate".upper():
    query_injury_rate_street = f"""
    SELECT
        STREET_NAME, COUNT(INJURIES_TOTAL > 0)*100/count(CRASH_RECORD_ID) as INJURY_RATE,
        COUNT(CRASH_RECORD_ID) as total_crashes

    FROM
        {TABLE_NAME}

    GROUP BY STREET_NAME
    HAVING COUNT(CRASH_RECORD_ID) > 100
    ORDER BY total_crashes DESC
    LIMIT {TOP_5};
    """
    df= pd.read_sql(query_injury_rate_street, conn)
    st.subheader("top 5 streets with highest injury rate:".upper())
    st.dataframe(df)
    st.write("Certain streets show a high proportion of injury-related crashes, marking them as critical areas for road safety improvements.")
    st.bar_chart(df.set_index("STREET_NAME")["total_crashes"])

elif case_study=="10. most common crash type by year".upper():
    query_crash_by_year = f"""
    SELECT year, FIRST_CRASH_TYPE, COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES,
        RANK() OVER(PARTITION BY year ORDER BY COUNT(CRASH_RECORD_ID) DESC) AS RANKS
        FROM {TABLE_NAME}
        GROUP BY year, FIRST_CRASH_TYPE;
    """
    df =pd.read_sql(query_crash_by_year, conn)
    st.subheader("Most Common Crash Type by year:".upper())
    st.dataframe(df)
    st.write("Yearly trends show shifts in dominant crash types, reflecting evolving traffic conditions and behavioral changes over time.")
    st.bar_chart(df.set_index("FIRST_CRASH_TYPE")["TOTAL_CRASHES"])

elif case_study == "11. day of the week with the highest average crashes per hour".upper():
    query_day_week = f"""
    SELECT CRASH_DAY_OF_WEEK, AVG(CRASH_HOUR) AS AVG_CRASH_HOUR
    FROM {TABLE_NAME}
    GROUP BY CRASH_DAY_OF_WEEK
    ORDER BY AVG_CRASH_HOUR DESC;
    """
    df= pd.read_sql(query_day_week, conn)
    st.subheader("Crash Distribution by Day of the Week:".upper())
    st.dataframe(df)
    st.write("Specific days of the week show consistently higher crash intensity, indicating predictable weekly traffic risk cycles.")


elif case_study =="12. Identifying high-risk time slots".upper():
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

    df= pd.read_sql(query_high_risk_time, conn)
    st.subheader("High-risk time slots:".upper())
    st.dataframe(df)
    st.write("Certain time intervals during the day consistently experience more crashes, highlighting peak-risk driving periods.")
    st.bar_chart(df.set_index("TIME_SLOT")["TOTAL_INJURY_CRASHES"])


elif case_study == "13. top 3 contributing causes for each crash type".upper():
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

    df = pd.read_sql(query_contributing_cause, conn)
    st.subheader("Top 3 contributing causes:".upper())
    st.dataframe(df)
    st.write("Contributing factors vary across crash types, revealing underlying behavioral and environmental causes of accidents.")


elif case_study == "14. year over year growth rate of crashes".upper():
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
    df = pd.read_sql(query_year_growth, conn)
    st.subheader("Year over year growth rate:".upper())
    st.dataframe(df)
    st.write("Annual crash trends show percentage changes over time, helping identify whether road safety conditions are improving or declining.")

elif case_study =="15. top 10 zone, grouped by locations".upper():
    query_zones = f"""
    SELECT ROUND(LATITUDE, 2) as R_LATITUDE, ROUND(LONGITUDE,2) as R_LONGITUDE,
    COUNT(CRASH_RECORD_ID) AS TOTAL_CRASHES
    FROM {TABLE_NAME}
    GROUP BY R_LATITUDE, R_LONGITUDE
    ORDER BY TOTAL_CRASHES DESC
    LIMIT {TOP_10};
    """
    df =pd.read_sql(query_zones, conn)
    st.subheader("Top 10 zone by locations:".upper())
    st.dataframe(df)
    st.write("Geographic clustering identifies concentrated crash zones, enabling targeted enforcement and infrastructure planning.")


