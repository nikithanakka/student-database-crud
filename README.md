
# Student Database CRUD Application

## Project Description
A Student Database CRUD Application built using Python, FastAPI, and SQLite. It allows users to create, view, update, and delete student records through REST API endpoints.

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn
- Swagger UI

## Features
- Add a new student
- View all students
- View a student by ID
- Update student details
- Delete a student record
- Prevent duplicate email addresses
- Handle errors for missing student records

## Project Structure
```text
student-database-crud/
├── main.py
├── database.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
python -m uvicorn main:app --reload
```

### 3. Open Swagger UI
Visit:
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Check API status |
| POST | /students | Create a student |
| GET | /students | View all students |
| GET | /students/{student_id} | View one student |
| PUT | /students/{student_id} | Update a student |
| DELETE | /students/{student_id} | Delete a student |

## Testing
The API endpoints were tested using Swagger UI. Create, Read, Update, and Delete operations returned successful responses during testing.

## Conclusion
This project demonstrates basic database management operations using a REST API built with Python, FastAPI, and SQLite.
