
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
import sqlite3

from database import get_connection, create_table

app = FastAPI(title="Student Database CRUD Application")

create_table()


# Request model for creating a student
class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    date_of_birth: str
    email: str
    phone: str | None = None


# Request model for updating a student
class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    date_of_birth: str | None = None
    email: str | None = None
    phone: str | None = None


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Student Database CRUD API is running!"
    }


# CREATE: Add a new student
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO students (name, date_of_birth, email, phone)
            VALUES (?, ?, ?, ?)
            """,
            (
                student.name,
                student.date_of_birth,
                student.email,
                student.phone,
            ),
        )

        connection.commit()

        return {
            "message": "Student created successfully",
            "student_id": cursor.lastrowid,
            "name": student.name,
            "email": student.email,
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    finally:
        connection.close()


# READ: Get all students
@app.get("/students")
def get_students():
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students ORDER BY id"
        )

        students = [dict(row) for row in cursor.fetchall()]

        return {
            "total": len(students),
            "students": students,
        }

    finally:
        connection.close()


# READ: Get one student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        )

        student = cursor.fetchone()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        return dict(student)

    finally:
        connection.close()


# UPDATE: Modify an existing student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        updates = student.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update",
            )

        for field in updates:
            if updates[field] is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"{field} cannot be null",
                )

        allowed_fields = {
            "name",
            "date_of_birth",
            "email",
            "phone",
        }

        if not set(updates).issubset(allowed_fields):
            raise HTTPException(
                status_code=400,
                detail="Invalid field",
            )

        set_clause = ", ".join(
            f"{field} = ?" for field in updates
        )

        values = list(updates.values()) + [student_id]

        connection.execute(
            f"UPDATE students SET {set_clause} WHERE id = ?",
            values,
        )

        connection.commit()

        updated = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        return {
            "message": "Student updated successfully",
            "student": dict(updated),
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    finally:
        connection.close()


# DELETE: Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        connection.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )

        connection.commit()

        return {
            "message": "Student deleted successfully",
            "student_id": student_id,
        }

    finally:
        connection.close()
