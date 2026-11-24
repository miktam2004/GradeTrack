import pandas as pd

mat = pd.read_csv(
    r"C:\Users\DELL\OneDrive\Desktop\student-api\dataset\student\student-mat.csv",
    sep=";"
)

por = pd.read_csv(
    r"C:\Users\DELL\OneDrive\Desktop\student-api\dataset\student\student-por.csv",
    sep=";"
)

# Combine both datasets
data = pd.concat([mat, por], ignore_index=True)

# Remove duplicate students
data = data.drop_duplicates(
    subset=[
        "school", "sex", "age", "address",
        "famsize", "Pstatus", "Medu", "Fedu",
        "Mjob", "Fjob", "reason", "nursery", "internet"
    ]
)

# Select only columns used by our MySQL table
data = data[
    [
        "school",
        "sex",
        "age",
        "address",
        "studytime",
        "failures",
        "internet",
        "activities",
        "absences",
        "G1",
        "G2",
        "G3"
    ]
]

# Rename columns
data = data.rename(columns={
    "sex": "gender",
    "studytime": "study_time",
    "G1": "grade_1",
    "G2": "grade_2",
    "G3": "final_grade"
})

print("Total rows ready for MySQL:", len(data))
print(data.head())

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jarvis259",
    database="student_db"
)

cursor = connection.cursor()

sql = """
    INSERT INTO students
    (school, gender, age, address, study_time, failures,
     internet, activities, absences, grade_1, grade_2, final_grade)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = [
    tuple(row)
    for row in data.itertuples(index=False, name=None)
]

cursor.executemany(sql, values)

connection.commit()

print("Students inserted:", cursor.rowcount)

cursor.close()
connection.close()