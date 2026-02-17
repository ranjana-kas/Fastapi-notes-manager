# Notes Manager API 📝

A clean, asynchronous REST API built with **FastAPI** to manage notes. 
This microservice demonstrates modern Python practices, including Pydantic validation, TypedDict models, and modular architecture.

## 🚀 Features
- **Create Notes:** Add new notes with titles and content.
- **Read Notes:** View all notes or retrieve a specific one by ID.
- **Update Notes:** Modify existing notes.
- **Delete Notes:** Remove notes from the system.
- **In-Memory Storage:** Uses a high-performance Python list structure (simulating a DB).

## 🛠️ Tech Stack
- **Python 3.9+**
- **FastAPI** (Web Framework)
- **Uvicorn** (ASGI Server)
- **Pydantic** (Data Validation)

## 📦 Installation

1. **Clone the repository** (or create the folder):
   ```bash
   mkdir notes_api
   cd notes_api

2. **install dependecies**
    ```bash
    pip install fastapi uvicorn

## 📖 API Documentation
- FastAPI provides automatic interactive documentation.
- Once the server is running, visit:

- Swagger UI: http://127.0.0.1:8000/docs

