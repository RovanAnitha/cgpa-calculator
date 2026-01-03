from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.main import main
from app.models import db, Student, Semester, Course
from app.main.forms import StudentForm, SemesterForm, CourseForm

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.filter_by(user_id=current_user.id).all()
    return render_template('main/dashboard.html', students=students)


@main.route('/students/new', methods=['GET', 'POST'])
@login_required
def create_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            user_id=current_user.id,
            name=form.name.data,
            student_id=form.student_id.data,
            email=form.email.data,
            program=form.program.data,
            year=form.year.data
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Student {student.name} created successfully!', 'success')
        return redirect(url_for('main.view_student', id=student.id))

    return render_template('main/student_form.html', form=form, title='Add Student')


@main.route('/students/<int:id>')
@login_required
def view_student(id):
    student = Student.query.get_or_404(id)
    if student.user_id != current_user.id:
        abort(403)
    return render_template('main/student_detail.html', student=student)


@main.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    if student.user_id != current_user.id:
        abort(403)

    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.student_id = form.student_id.data
        student.email = form.email.data
        student.program = form.program.data
        student.year = form.year.data
        db.session.commit()
        flash(f'Student {student.name} updated successfully!', 'success')
        return redirect(url_for('main.view_student', id=student.id))

    return render_template('main/student_form.html', form=form, title='Edit Student')


@main.route('/students/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    if student.user_id != current_user.id:
        abort(403)

    name = student.name
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {name} deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/students/<int:student_id>/semesters/new', methods=['GET', 'POST'])
@login_required
def create_semester(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        abort(403)

    form = SemesterForm()
    if form.validate_on_submit():
        semester = Semester(
            student_id=student.id,
            name=form.name.data,
            semester_number=form.semester_number.data,
            year=form.year.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(semester)
        db.session.commit()
        flash(f'Semester {semester.name} created successfully!', 'success')
        return redirect(url_for('main.view_semester', id=semester.id))

    return render_template('main/semester_form.html', form=form, student=student, title='Add Semester')


@main.route('/semesters/<int:id>')
@login_required
def view_semester(id):
    semester = Semester.query.get_or_404(id)
    if semester.student.user_id != current_user.id:
        abort(403)
    return render_template('main/semester_detail.html', semester=semester)


@main.route('/semesters/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_semester(id):
    semester = Semester.query.get_or_404(id)
    if semester.student.user_id != current_user.id:
        abort(403)

    form = SemesterForm(obj=semester)
    if form.validate_on_submit():
        semester.name = form.name.data
        semester.semester_number = form.semester_number.data
        semester.year = form.year.data
        semester.start_date = form.start_date.data
        semester.end_date = form.end_date.data
        db.session.commit()
        flash(f'Semester {semester.name} updated successfully!', 'success')
        return redirect(url_for('main.view_semester', id=semester.id))

    return render_template('main/semester_form.html', form=form, student=semester.student, title='Edit Semester')


@main.route('/semesters/<int:id>/delete', methods=['POST'])
@login_required
def delete_semester(id):
    semester = Semester.query.get_or_404(id)
    if semester.student.user_id != current_user.id:
        abort(403)

    student_id = semester.student_id
    name = semester.name
    db.session.delete(semester)
    db.session.commit()
    flash(f'Semester {name} deleted successfully!', 'success')
    return redirect(url_for('main.view_student', id=student_id))


@main.route('/semesters/<int:semester_id>/courses/new', methods=['GET', 'POST'])
@login_required
def create_course(semester_id):
    semester = Semester.query.get_or_404(semester_id)
    if semester.student.user_id != current_user.id:
        abort(403)

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            semester_id=semester.id,
            course_name=form.course_name.data,
            subject_area=form.subject_area.data,
            course_code=form.course_code.data,
            credits=form.credits.data,
            marks=form.marks.data
        )
        db.session.add(course)
        db.session.commit()
        flash(f'Course {course.course_name} added successfully!', 'success')
        return redirect(url_for('main.view_semester', id=semester.id))

    return render_template('main/course_form.html', form=form, semester=semester, title='Add Course')


@main.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    if course.semester.student.user_id != current_user.id:
        abort(403)

    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.course_name = form.course_name.data
        course.subject_area = form.subject_area.data
        course.course_code = form.course_code.data
        course.credits = form.credits.data
        course.marks = form.marks.data
        db.session.commit()
        flash(f'Course {course.course_name} updated successfully!', 'success')
        return redirect(url_for('main.view_semester', id=course.semester_id))

    return render_template('main/course_form.html', form=form, semester=course.semester, title='Edit Course')


@main.route('/courses/<int:id>/delete', methods=['POST'])
@login_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    if course.semester.student.user_id != current_user.id:
        abort(403)

    semester_id = course.semester_id
    name = course.course_name
    db.session.delete(course)
    db.session.commit()
    flash(f'Course {name} deleted successfully!', 'success')
    return redirect(url_for('main.view_semester', id=semester_id))
