import pandas as pd

df = pd.read_csv("dataset/student/student-mat.csv", sep=";")

print("Number of students:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 students:")
print(df.head())