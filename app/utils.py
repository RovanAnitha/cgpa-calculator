def marks_to_grade_point(marks):
    """Convert marks (0-100) to grade point (10-point scale)"""
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    elif marks >= 30:
        return 4
    else:
        return 0


def calculate_semester_gpa(semester):
    """Calculate GPA for a single semester"""
    courses = semester.courses.all()

    if not courses:
        return 0.0

    total_credits = 0
    weighted_grade_points = 0

    for course in courses:
        credits = float(course.credits)
        grade_point = course.grade_point
        total_credits += credits
        weighted_grade_points += (grade_point * credits)

    if total_credits == 0:
        return 0.0

    return round(weighted_grade_points / total_credits, 2)


def calculate_overall_cgpa(student):
    """Calculate overall CGPA across all semesters for a student"""
    semesters = student.semesters.all()

    if not semesters:
        return 0.0

    total_credits = 0
    weighted_gpa = 0

    for semester in semesters:
        semester_credits = semester.total_credits
        semester_gpa = semester.gpa

        if semester_credits > 0:
            total_credits += semester_credits
            weighted_gpa += (semester_gpa * semester_credits)

    if total_credits == 0:
        return 0.0

    return round(weighted_gpa / total_credits, 2)
