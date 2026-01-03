# CGPA Calculator - Flask PostgreSQL Application

A full-stack web application for managing student CGPA records with multi-user authentication and PostgreSQL database.

## Features

- User authentication (registration, login, logout)
- Multi-user support with data isolation
- Student management
- Semester organization
- Course tracking with marks and credits
- Automatic GPA and CGPA calculations
- Beautiful pink gradient UI
- Responsive design

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Make sure PostgreSQL is running and create the database:

```bash
psql -U postgres
CREATE DATABASE cgpa_calculator;
\q
```

### 3. Configure Environment Variables

Edit the `.env` file and update your database credentials:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/cgpa_calculator
FLASK_APP=run.py
FLASK_ENV=development
```

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Initialize Database

```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration
flask db migrate -m "Initial migration: users, students, semesters, courses"

# Apply migration to database
flask db upgrade
```

### 5. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### First Time Setup

1. Navigate to `http://localhost:5000/auth/register`
2. Create a new account
3. Log in with your credentials
4. Start adding students!

### Workflow

1. **Add a Student**: Create a student profile with name, ID, program, etc.
2. **Add Semesters**: Organize courses by academic term
3. **Add Courses**: Enter course details with credits and marks
4. **View CGPA**: Automatically calculated based on all courses

## Grade Scale (10-Point System)

| Marks Range | Grade Point |
|-------------|-------------|
| 90-100      | 10          |
| 80-89       | 9           |
| 70-79       | 8           |
| 60-69       | 7           |
| 50-59       | 6           |
| 40-49       | 5           |
| 30-39       | 4           |
| 0-29        | 0           |

## CGPA Calculation

**Semester GPA:**
```
GPA = Σ(grade_point × credits) / Σ(credits)
```

**Overall CGPA:**
```
CGPA = Σ(semester_gpa × semester_credits) / Σ(semester_credits)
```

## Project Structure

```
cgpa-calculator/
├── app/
│   ├── auth/              # Authentication blueprint
│   ├── main/              # Main application blueprint
│   ├── static/            # CSS and JavaScript
│   ├── templates/         # Jinja2 templates
│   ├── __init__.py       # Flask app factory
│   ├── models.py         # Database models
│   └── utils.py          # Utility functions
├── migrations/            # Database migrations
├── config.py             # Configuration
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## Database Models

- **User**: Authentication and user management
- **Student**: Student profiles
- **Semester**: Academic terms
- **Course**: Individual courses with marks and credits

## Security Features

- Password hashing (PBKDF2-SHA256)
- CSRF protection on all forms
- SQL injection prevention (SQLAlchemy ORM)
- User authorization (users can only access their own data)
- Session security with secure cookies

## Troubleshooting

### Database Connection Error

Make sure PostgreSQL is running and credentials in `.env` are correct:

```bash
psql -U postgres -c "SELECT version();"
```

### Migration Issues

If you encounter migration errors, you can reset:

```bash
flask db downgrade
flask db upgrade
```

### Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows CMD
$env:FLASK_ENV="development"  # Windows PowerShell

python run.py
```

### Database Shell

Access the Flask shell to interact with the database:

```bash
flask shell
```

```python
# Example: Create a test user
from app.models import User, db
user = User(username='test', email='test@example.com')
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

## Contributing

This project was built with Claude Code. Feel free to enhance and customize!

## License

MIT License
