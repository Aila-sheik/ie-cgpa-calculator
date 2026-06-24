# Standard 10-point scale mapping
GRADE_POINTS = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'B': 6,
    'C': 5,
    'U': 0
}

def get_grade_point(grade_input):
    grade = grade_input.strip().upper()
    if grade in GRADE_POINTS:
        return GRADE_POINTS[grade]
    return None