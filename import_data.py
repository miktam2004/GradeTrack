import pandas as pd
import mysql.connector

# Read CSV
df = pd.read_csv(
    "dataset/student/student-mat.csv",
    sep=";"
)

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jarvis259",
    database="student_db"
)

cursor = connection.cursor()

# SQL query
sql = """
    INSERT INTO students
    (school, gender, age, address, study_time, failures,
     internet, activities, absences, grade_1, grade_2, final_grade)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert each student
for _, row in df.iterrows():

    values = (
        row["school"],
        row["sex"],
        row["age"],
        row["address"],
        row["studytime"],
        row["failures"],
        row["internet"],
        row["activities"],
        row["absences"],
        row["G1"],
        row["G2"],
        row["G3"]
    )

    cursor.execute(sql, values)

connection.commit()

print(f"{len(df)} students imported successfully!")

cursor.close()
connection.close()