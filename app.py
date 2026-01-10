import csv
import sys

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

def calculate_cgpa(csv_file):
    """Calculate CGPA from CSV file containing course data"""
    try:
        total_credits = 0
        weighted_grade_points = 0
        courses = []

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            print("\n" + "="*90)
            print(f"{'Course Name':<30} {'Subject Area':<20} {'Credits':<10} {'Marks':<10} {'Grade Point':<10}")
            print("="*90)

            for row in reader:
                course_name = row['Course Name']
                subject_area = row.get('Subject Area', 'N/A')
                credits = float(row['Credits'])
                marks = float(row['Marks'])

                grade_point = marks_to_grade_point(marks)

                courses.append({
                    'name': course_name,
                    'subject': subject_area,
                    'credits': credits,
                    'marks': marks,
                    'grade_point': grade_point
                })

                total_credits += credits
                weighted_grade_points += (grade_point * credits)

                print(f"{course_name:<30} {subject_area:<20} {credits:<10.1f} {marks:<10.1f} {grade_point:<10.1f}")

            print("="*90)

            if total_credits > 0:
                cgpa = weighted_grade_points / total_credits
                print(f"\nTotal Credits: {total_credits:.1f}")
                print(f"CGPA: {cgpa:.2f}")
                print("="*90 + "\n")
                return cgpa
            else:
                print("\nError: No courses found or total credits is zero.")
                return None

    except FileNotFoundError:
        print(f"\nError: File '{csv_file}' not found.")
        print("Please create a CSV file with columns: Course Name, Subject Area, Credits, Marks")
        return None
    except KeyError as e:
        print(f"\nError: Missing required column {e} in CSV file.")
        print("CSV file must have columns: Course Name, Subject Area (optional), Credits, Marks")
        return None
    except ValueError as e:
        print(f"\nError: Invalid data in CSV file - {e}")
        print("Credits and Marks must be numeric values.")
        return None

if __name__ == "__main__":
    csv_file = "courses.csv"

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    print("\n*** CGPA Calculator (10-Point Scale) ***")
    print(f"Reading from: {csv_file}\n")
    calculate_cgpa(csv_file)
