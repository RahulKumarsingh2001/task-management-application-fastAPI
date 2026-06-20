# 🚀 Task Management API (FastAPI)

## 📌 Project Description

This is a backend project built using FastAPI. It provides APIs for user authentication and task management. Users can register, login, and manage their tasks.

---

## 🛠️ Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Alembic
* SQLite / PostgreSQL

---

## 📂 Project Setup Guide

Follow these steps to run this project in your local machine (VS Code):

---

## 1️⃣ Clone the Repository

Open terminal in VS Code and run:

git clone https://github.com/your-username/task-management-app.git

cd task-management-app

---

## 2️⃣ Open in VS Code

Open the project folder in VS Code:

code .

---

## 3️⃣ Create Virtual Environment

python -m venv env

---

## 4️⃣ Activate Virtual Environment

For Mac/Linux:

source env/bin/activate

For Windows:

env\Scripts\activate

---

## 5️⃣ Install Dependencies

pip install -r requirements.txt

---

## 6️⃣ Setup Environment Variables

Create a `.env` file in root folder and add:

DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

---

## 7️⃣ Run Database Migrations

alembic upgrade head

---

## 8️⃣ Run the Server

uvicorn main:app --reload

---

## 🌐 Access API

Open browser and go to:

http://127.0.0.1:8000/docs

This will open Swagger UI where you can test APIs.

---

## 📡 API Endpoints

### User APIs

* POST /user/register
* POST /user/login
* GET /user/is_auth

### Task APIs

* Create Task
* Update Task
* Delete Task

---

## 📌 Notes

* Make sure Python is installed (version 3.8+)
* Always activate virtual environment before running project
* Do not upload your `.env` file to GitHub

---

## 🙌 Contribution

Feel free to fork this repository and improve the project.

---

## 📧 Contact

Your Name
