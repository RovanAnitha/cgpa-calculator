from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length, ValidationError
from app.models import Student

class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[
        DataRequired(),
        Length(max=100, message='Name must be less than 100 characters')
    ])
    student_id = StringField('Student ID', validators=[
        DataRequired(),
        Length(max=50, message='Student ID must be less than 50 characters')
    ])
    email = StringField('Email', validators=[
        Optional(),
        Email(message='Invalid email address')
    ])
    program = StringField('Program', validators=[
        Optional(),
        Length(max=100, message='Program name must be less than 100 characters')
    ])
    year = IntegerField('Year', validators=[Optional()])
    submit = SubmitField('Save Student')


class SemesterForm(FlaskForm):
    name = StringField('Semester Name', validators=[
        DataRequired(),
        Length(max=50, message='Name must be less than 50 characters')
    ])
    semester_number = IntegerField('Semester Number', validators=[
        DataRequired(),
        NumberRange(min=1, message='Semester number must be at least 1')
    ])
    year = IntegerField('Year', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Save Semester')


class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[
        DataRequired(),
        Length(max=200, message='Course name must be less than 200 characters')
    ])
    subject_area = SelectField('Subject Area', choices=[
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Electronics', 'Electronics'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Humanities', 'Humanities'),
        ('Business', 'Business'),
        ('Other', 'Other')
    ], validators=[Optional()])
    course_code = StringField('Course Code', validators=[
        Optional(),
        Length(max=50, message='Course code must be less than 50 characters')
    ])
    credits = DecimalField('Credits', validators=[
        DataRequired(),
        NumberRange(min=0.5, max=10, message='Credits must be between 0.5 and 10')
    ], places=2)
    marks = DecimalField('Marks (0-100)', validators=[
        DataRequired(),
        NumberRange(min=0, max=100, message='Marks must be between 0 and 100')
    ], places=2)
    submit = SubmitField('Save Course')
