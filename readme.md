# Task Management Application — FastAPI

A production-style backend REST API built with **FastAPI** that lets users register, log in with JWT authentication, and perform full CRUD operations on their personal tasks. The project follows a clean, modular architecture (router → controller → model/DTO) and uses **SQLAlchemy** with **Alembic** for database modelling and migrations, plus **FastAPI-Mail** for transactional emails.

---

## 📌 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Tech Stack](#-tech-stack)
4. [Project Architecture](#-project-architecture)
5. [Folder Structure](#-folder-structure)
6. [Database Schema](#-database-schema)
7. [Environment Variables](#-environment-variables)
8. [API Endpoints](#-api-endpoints)
9. [Authentication Flow](#-authentication-flow)
10. [Local Setup Guide](#-local-setup-guide)
11. [Running Migrations](#-running-database-migrations-alembic)
12. [Testing the API](#-testing-the-api)
13. [Notes & Best Practices](#-notes--best-practices)
14. [Contributing](#-contributing)
15. [License & Contact](#-license--contact)

---

## 🔎 Overview

This project is a **Task Management REST API** where each authenticated user can manage their own list of tasks. It demonstrates real-world backend concepts: layered architecture, ORM modelling, relational integrity (foreign keys with `ON DELETE CASCADE`), password hashing with **Argon2**, **JWT** based authentication, request validation with **Pydantic v2**, schema migrations with **Alembic**, and asynchronous email delivery using **FastAPI-Mail**.

---

## ✨ Key Features

- 🔐 **User Registration & Login** with hashed passwords (Argon2 via `pwdlib`)
- 🪪 **JWT Authentication** (`PyJWT`) with configurable expiry
- 📨 **Welcome Email** on registration via `fastapi-mail` (async SMTP)
- 📝 **Task CRUD** — create, list, fetch one, update, delete
- 👤 **Per-user authorization** — users can only mutate their own tasks
- 🗄️ **PostgreSQL** support via `psycopg2-binary`
- 🧬 **Alembic Migrations** for versioned schema changes
- 📜 **Auto-generated Swagger / OpenAPI Docs** at `/docs`
- 🧩 **Modular structure** (routers, controllers, DTOs, models, utils)

---

## 🛠 Tech Stack

| Layer            | Technology                                                  |
| ---------------- | ----------------------------------------------------------- |
| Language         | Python 3.8+                                                 |
| Web Framework    | FastAPI 0.136                                               |
| ASGI Server      | Uvicorn                                                     |
| ORM              | SQLAlchemy 2.0                                              |
| Migrations       | Alembic                                                     |
| Database         | PostgreSQL (configurable; works with any SQLAlchemy URL)    |
| Validation       | Pydantic v2 + `pydantic-settings`                           |
| Auth             | PyJWT (HS256) + Argon2 password hashing (`pwdlib`)          |
| Email            | FastAPI-Mail + aiosmtplib                                   |
| Config           | python-dotenv / Pydantic Settings                           |

---

## 🏗 Project Architecture

The project follows a **3-layer modular architecture** per domain (users, tasks):

```
HTTP Request
    │
    ▼
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Router    │ ───► │  Controller  │ ───► │   Model    │
│  (FastAPI)  │      │  (business)  │      │ (SQLAlch.) │
└─────────────┘      └──────────────┘      └────────────┘
       ▲                    │
       │                    ▼
   DTO (Pydantic)      Database (PostgreSQL)
```

- **Router** — declares HTTP endpoints, request/response models, and dependencies (`get_db`, `is_authenticated`).
- **Controller** — pure business logic, talks to the DB session.
- **DTOs** — Pydantic schemas for input validation and response shaping.
- **Models** — SQLAlchemy ORM tables.
- **Utils** — DB session factory, settings loader, helpers, email service.

---

## 📂 Folder Structure

```
task-management-application-fastAPI/
│
├── main.py                     # FastAPI app entry point, router registration
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
│
├── migrations/                 # Alembic migration scripts
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 64b7448a08ae_add_user_id_to_tasks.py
│
└── src/
    ├── tasks/
    │   ├── router.py           # /tasks endpoints
    │   ├── controller.py       # Task business logic
    │   ├── models.py           # TaskModel (user_tasks table)
    │   └── dtos.py             # TaskSchema, TaskResponseSchema
    │
    ├── users/
    │   ├── router.py           # /user endpoints
    │   ├── controller.py       # Register, login, JWT auth
    │   ├── models.py           # UserModel (user_table)
    │   └── dtos.py             # UserSchema, LoginSchema, UserResponseSchema
    │
    └── utils/
        ├── db.py               # SQLAlchemy engine, session, Base, get_db
        ├── setting.py          # Pydantic settings loader (.env)
        ├── email.py            # FastAPI-Mail send_email helper
        ├── helpers.py          # is_authenticated dependency
        └── constant.py
```

---

## 🗄 Database Schema

**`user_table`**

| Column          | Type    | Constraints           |
| --------------- | ------- | --------------------- |
| id              | Integer | PK                    |
| name            | String  |                       |
| username        | String  | NOT NULL              |
| hash_password   | String  | NOT NULL (Argon2)     |
| email           | String  |                       |

**`user_tasks`**

| Column        | Type    | Constraints                                          |
| ------------- | ------- | ---------------------------------------------------- |
| id            | Integer | PK                                                   |
| title         | String  |                                                      |
| description   | String  |                                                      |
| is_completed  | Boolean | default `False`                                      |
| user_id       | Integer | FK → `user_table.id` `ON DELETE CASCADE`             |

Deleting a user automatically cascades and removes all their tasks.

---

## 🔐 Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
DB_CONNECTION_URI=postgresql://<user>:<password>@<host>:<port>/<database>
JWT_SECRET_KEY=your-long-random-secret
JWT_ALGORITHM=HS256
EXP_TIME=30          # JWT expiry in minutes
```

If you use FastAPI-Mail, you will also need standard SMTP variables (host, port, username, password, from-address) used inside `src/utils/email.py`.

---

## 📡 API Endpoints

Base URL: `http://127.0.0.1:8000`

### 👤 User

| Method | Endpoint           | Description                            | Auth |
| ------ | ------------------ | -------------------------------------- | ---- |
| POST   | `/user/register`   | Register a new user, sends welcome email | ❌  |
| POST   | `/user/login`      | Login, returns JWT access token        | ❌   |
| GET    | `/user/is_auth`    | Returns the current authenticated user | ✅   |

### ✅ Tasks (all require JWT)

| Method | Endpoint                      | Description                       |
| ------ | ----------------------------- | --------------------------------- |
| POST   | `/tasks/create`               | Create a new task for current user |
| GET    | `/tasks/all_tasks`            | List all tasks of current user     |
| GET    | `/tasks/one_task/{task_id}`   | Get a single task                  |
| PUT    | `/tasks/update_task/{task_id}`| Update a task (owner only)         |
| DELETE | `/tasks/delete_task/{task_id}`| Delete a task (owner only)         |

Pass the token in headers:

```
Authorization: Bearer <jwt_token>
```

---

## 🔁 Authentication Flow

1. **Register** → password is hashed with Argon2 and stored.
2. **Login** → credentials are verified; server returns a signed JWT containing `_id` and `exp`.
3. **Protected request** → client sends `Authorization: Bearer <token>`.
4. `is_authenticated` dependency decodes the token, loads the user from DB, and injects the `UserModel` into the endpoint.
5. Controllers enforce per-user ownership on update/delete.

---

## 💻 Local Setup Guide

Follow these steps to run the project locally (works on Windows, macOS, and Linux).

### ✅ Prerequisites

- Python **3.8+**
- pip
- PostgreSQL running locally (or any SQLAlchemy-compatible DB)
- Git
- (Recommended) Visual Studio Code

### 1️⃣ Clone the repository

```bash
git clone https://github.com/RahulKumarsingh2001/task-management-application-fastAPI.git
cd task-management-application-fastAPI
```

### 2️⃣ Create & activate a virtual environment

```bash
# Create
python -m venv env

# Activate — macOS / Linux
source env/bin/activate

# Activate — Windows (PowerShell)
env\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

```bash
cp .env.example .env       # macOS / Linux
copy .env.example .env     # Windows
```

Then edit `.env` and set `DB_CONNECTION_URI`, `JWT_SECRET_KEY`, etc.

### 5️⃣ Create the database

Make sure the database referenced in `DB_CONNECTION_URI` exists, e.g.:

```sql
CREATE DATABASE task_db;
```

### 6️⃣ Run database migrations

```bash
alembic upgrade head
```

### 7️⃣ Start the development server

```bash
uvicorn main:app --reload
```

The API is now live at: **http://127.0.0.1:8000**

---

## 🧬 Running Database Migrations (Alembic)

Create a new migration after changing models:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

Roll back the last migration:

```bash
alembic downgrade -1
```

---

## 🧪 Testing the API

FastAPI auto-generates interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can also use **Postman**, **Insomnia**, or `curl`:

```bash
# Register
curl -X POST http://127.0.0.1:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul","username":"rahul","password":"secret","email":"rahul@example.com"}'

# Login
curl -X POST http://127.0.0.1:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul","username":"rahul","password":"secret"}'

# Create task (use the returned token)
curl -X POST http://127.0.0.1:8000/tasks/create \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Read docs","description":"Read FastAPI docs","is_completed":false}'
```

---

## 📝 Notes & Best Practices

- ❗ **Never commit your `.env`** file — it contains secrets.
- 🔑 Use a strong, random `JWT_SECRET_KEY` in production (e.g. `openssl rand -hex 32`).
- 🗃 Always run `alembic upgrade head` after pulling new model changes.
- 🐍 Always activate the virtual environment before installing packages or running the server.
- 🚀 In production, run with a process manager:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
  ```
- 📧 Configure proper SMTP credentials before testing the registration email flow.

---

## 🤝 Contributing

Contributions are very welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License & Contact

This project is open-source and free to use for learning purposes.

**Author:** Rahul Kumar Singh
**GitHub:** [@RahulKumarsingh2001](https://github.com/RahulKumarsingh2001)

If you found this project helpful, consider giving it a ⭐ on GitHub!
