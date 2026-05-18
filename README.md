# Traffic-Crash-Analysis

## Overview
This project analyzes traffic crash data using Python, SQL, Pandas, Matplotlib, and Streamlit.  The goal of the project is to identify accident trends, high-risk areas, and crash patterns using data analysis and visualizations.

---

## Tools & Technologies Used

- Python
- Pandas
- SQLite3
- Matplotlib
- Streamlit
- PyCharm

---

## Features

- Traffic crash data analysis using Python
- Data querying using Pandas and SQLite3
- Data visualization using Matplotlib
- Interactive dashboard development using Streamlit
- Accident trend and severity analysis

---

## Project Structure

```bash

Traffic-Crash-Analytics/
│
├── data/
│   └── Traffic Crash Analytics & Safety Intelligence Platform.pdf
│   
│
├── app/
│   └── app.py
│
├── querying/
│   └── Project.py
│
├── requirements.txt
└── README.md
```

## Database Setup

Before running the project, create a SQLite3 database file named:

```bash
Crash_Project.db
```

Run the following Python code to create the database and import the CSV dataset into SQLite3:

```python
import pandas as pd
import sqlite3

# Load dataset
df = pd.read_csv("data/Traffic_CrashesData.csv")

# Create SQLite database
conn = sqlite3.connect("data/Crash_Project.db")

# Store data into database table
df.to_sql("traffic_crashes", conn, if_exists="replace", index=False)

print("Database created successfully.")
```

## Conclusion

This project analyzes traffic crash data using Python, Pandas, SQLite3, Matplotlib, and Streamlit. It helps identify accident trends and severity patterns through visualizations and an interactive dashboard. The project demonstrates practical skills in data analysis and dashboard development using Python.

