User Authentication System
A robust and scalable user authentication backend built with FastAPI, SQLModel, and Pydantic v2. This system implements industry-standard security practices for user registration, login, and account management.

Key Features
JWT Authentication: Secure login and authorization using JSON Web Tokens.
Email Verification: Asynchronous account verification via background tasks.
Automatic Database Initialization: Automatic table generation on startup using FastAPI lifespan events.
Layered Dependency Injection: Granular access control through specialized dependencies (ActiveUser, VerifiedUser).
Global Exception Handling: Centralized error management to ensure consistent API responses.
Security Best Practices: Password hashing with Passlib (Bcrypt) and environment-based configuration.

Technical Stack
Backend Framework: FastAPI
Database Toolkit: SQLModel (SQLAlchemy + Pydantic integration)
Database: SQLite (default) or PostgreSQL
Security: PyJWT for token management, Passlib for hashing
Environment Management: Python-dotenv

Installation
1. Clone the repository
git clone https://github.com/NghiaNguyxn/User-Authentication-System.git
cd repository-name
2. Set up a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configuration
Create a .env file from the provided template:
cp .env.example .env
Edit the .env file to include your specific configurations such as SECRET_KEY, DATABASE_URL, and MAIL settings for email verification.
Running the Application
Start the server:
python run.py
Access the interactive API documentation:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

Project Structure

├── app/
│   ├── api/                # API Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication endpoints
│   │   └── user.py         # User management endpoints
│   ├── templates/          # Email or HTML templates
│   │   ├── reset_password.html # Template for password recovery emails
│   │   └── verify_email.html   # Template for account verification emails
│   ├── __init__.py
│   ├── config.py           # Configuration and Environment variables
│   ├── crud.py             # Database CRUD operations
│   ├── database.py         # Database engine and session setup
│   ├── dependencies.py     # FastAPI dependencies (Auth levels)
│   ├── email.py            # Email sending logic
│   ├── exception_handlers.py # Global exception mapping
│   ├── exceptions.py       # Custom exception classes
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # SQLModel database schemas
│   └── security.py         # Password hashing and JWT logic
├── venv/                   # Python virtual environment
├── .env                    # Private environment variables
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── create_db.py            # Manual script for DB creation (if needed)
├── database.db             # SQLite database file
├── LICENSE                 # Project license
├── README.md               # Project documentation
├── requirements.txt         # Project dependencies
└── run.py                  # Script to run the application

Security Implementation Note
This project uses the lifespan pattern to manage database connections and table creation. Sensitive data such as the SECRET_KEY and DATABASE_URL are never hardcoded in the source code; they must be managed through environment variables to ensure production security.

License
This project is licensed under the MIT License - see the LICENSE file for details.