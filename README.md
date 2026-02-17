# Notes Manager API 📝

A clean, asynchronous REST API built with **FastAPI** to manage notes. 
This microservice demonstrates modern Python practices, including Pydantic validation, TypedDict models, and modular architecture.

# 📝 Notes Manager (Full Stack)

A complete **Full Stack** application for managing notes. 
It features a high-performance REST API backend built with **FastAPI** and a modern, interactive frontend built with **Streamlit**.

## 🚀 Features

### Backend (FastAPI)
- **⚡ Async Architecture:** High-performance, non-blocking endpoints.
- **🔍 Advanced Search:** Instant filtering by title or content.
- **📄 Pagination:** Efficient handling of large lists.
- **🛡️ Data Validation:** Robust data integrity using Pydantic.
- **⚙️ Background Tasks:** Simulates heavy processing without freezing the app.

### Frontend (Streamlit)
- **🖥️ Interactive UI:** Clean, web-based interface.
- **✍️ Real-time Editing:** Create, edit, and delete notes instantly.
- **📱 Responsive:** Works on desktop and mobile browsers.

## 🛠️ Tech Stack
- **Python 3.9+**
- **FastAPI** (Backend API)
- **Uvicorn** (ASGI Server)
- **Streamlit** (Frontend UI)
- **Pydantic** (Data Validation)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [hhttps://github.com/ranjana-kas/Fastapi-notes-manager]
   cd fastapi-notes-manager



2. **install dependecies**
    ```bash
    pip install fastapi uvicorn

## 📖 API Documentation
- FastAPI provides automatic interactive documentation.
- Once the server is running, visit:

- Swagger UI: http://127.0.0.1:8000/docs

## start frontend and backend

- uvicorn main:app --reload
- streamlit run frontend.py