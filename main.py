from fastapi import FastAPI, HTTPException, Query ,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
import mysql.connector
from jose import jwt
from datetime import datetime, timedelta


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    school: str
    gender: str
    age: int = Field(..., ge=15, le=25)
    address: str
    study_time: int = Field(..., ge=1, le=4)
    failures: int = Field(..., ge=0, le=4)
    internet: str
    activities: str
    absences: int = Field(..., ge=0)
    grade_1: int = Field(..., ge=0, le=20)
    grade_2: int = Field(..., ge=0, le=20)
    final_grade: int = Field(..., ge=0, le=20)

class User(BaseModel):
    username: str
    password: str


SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm = Depends()):

    username = form_data.username
    password = form_data.password

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        user = cursor.fetchone()

        if user is None or password != user["password"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        token = create_token(username)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.post("/register", status_code=201)
def register(user: User):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            (user.username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (user.username, user.password)
        )

        connection.commit()

        return {
            "message": "User registered successfully",
            "id": cursor.lastrowid
        }

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_token(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jarvis259",
        database="student_db"
    )

@app.get("/")
def home():
    return {"message": "Student API is running"}


@app.get("/test-db")
def test_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT 1")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {"database": "connected", "result": result[0]}

@app.get("/students")
def get_students(
    current_user: str = Depends(verify_token),
    school: Optional[str] = None,
    gender: Optional[str] = None,
    min_grade: Optional[int] = Query(None, ge=0, le=20),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = "SELECT * FROM students WHERE 1=1"
        values = []

        if school:
            sql += " AND school = %s"
            values.append(school)

        if gender:
            sql += " AND gender = %s"
            values.append(gender)

        if min_grade is not None:
            sql += " AND final_grade >= %s"
            values.append(min_grade)

        sql += " LIMIT %s OFFSET %s"
        values.extend([limit, offset])

        cursor.execute(sql, values)

        return cursor.fetchall()

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    current_user: str = Depends(verify_token)
):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.post("/students", status_code=201)
def create_student(
    student: Student,
    current_user: str = Depends(verify_token)
):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO students
            (school, gender, age, address, study_time, failures,
             internet, activities, absences, grade_1, grade_2, final_grade)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            student.school,
            student.gender,
            student.age,
            student.address,
            student.study_time,
            student.failures,
            student.internet,
            student.activities,
            student.absences,
            student.grade_1,
            student.grade_2,
            student.final_grade
        )

        cursor.execute(sql, values)
        connection.commit()

        return {
            "message": "Student created successfully",
            "id": cursor.lastrowid
        }

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.put("/students/{student_id}", status_code=200)
def update_student(
    student_id: int,
    student: Student,
    current_user: str = Depends(verify_token)
):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
            UPDATE students
            SET school = %s,
                gender = %s,
                age = %s,
                address = %s,
                study_time = %s,
                failures = %s,
                internet = %s,
                activities = %s,
                absences = %s,
                grade_1 = %s,
                grade_2 = %s,
                final_grade = %s
            WHERE id = %s
        """

        values = (
            student.school,
            student.gender,
            student.age,
            student.address,
            student.study_time,
            student.failures,
            student.internet,
            student.activities,
            student.absences,
            student.grade_1,
            student.grade_2,
            student.final_grade,
            student_id
        )

        cursor.execute(sql, values)

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "message": "Student updated successfully",
            "id": student_id
        }

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    current_user: str = Depends(verify_token)
):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.get("/analytics/average-grade")
def average_grade():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT AVG(final_grade) FROM students"
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "average_final_grade": round(result[0], 2)
    }
@app.get("/analytics/top-students")
def top_students(
    limit: int = Query(10, ge=1, le=100)
):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, school, gender, age,
               grade_1, grade_2, final_grade
        FROM students
        ORDER BY final_grade DESC
        LIMIT %s
    """, (limit,))

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students

@app.get("/analytics/school-stats")
def school_stats():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            school,
            COUNT(*) AS total_students,
            ROUND(AVG(final_grade), 2) AS average_grade
        FROM students
        GROUP BY school
        ORDER BY average_grade DESC
    """)

    stats = cursor.fetchall()

    cursor.close()
    connection.close()

    return stats

@app.get("/analytics/absence-stats")
def absence_stats():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            MIN(absences) AS minimum_absences,
            MAX(absences) AS maximum_absences,
            ROUND(AVG(absences), 2) AS average_absences,
            SUM(CASE WHEN absences > 10 THEN 1 ELSE 0 END) AS students_above_10_absences
        FROM students
    """)

    stats = cursor.fetchone()

    cursor.close()
    connection.close()

    return stats