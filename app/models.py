from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    students = db.relationship('Student', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120))
    program = db.Column(db.String(100))
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    semesters = db.relationship('Semester', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def overall_cgpa(self):
        from app.utils import calculate_overall_cgpa
        return calculate_overall_cgpa(self)

    def __repr__(self):
        return f'<Student {self.name}>'


class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    semester_number = db.Column(db.Integer)
    year = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courses = db.relationship('Course', backref='semester', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'semester_number', name='uq_student_semester'),
    )

    @property
    def total_credits(self):
        return sum(float(course.credits) for course in self.courses.all())

    @property
    def gpa(self):
        from app.utils import calculate_semester_gpa
        return calculate_semester_gpa(self)

    def __repr__(self):
        return f'<Semester {self.name}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False, index=True)
    course_name = db.Column(db.String(200), nullable=False)
    subject_area = db.Column(db.String(100))
    course_code = db.Column(db.String(50))
    credits = db.Column(db.Numeric(4, 2), nullable=False)
    marks = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('marks >= 0 AND marks <= 100', name='check_marks_range'),
        CheckConstraint('credits > 0', name='check_credits_positive'),
    )

    @property
    def grade_point(self):
        from app.utils import marks_to_grade_point
        return marks_to_grade_point(float(self.marks))

    def __repr__(self):
        return f'<Course {self.course_name}>'
