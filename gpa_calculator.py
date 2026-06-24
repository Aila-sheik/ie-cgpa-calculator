def calculate_semester_gpa(subjects_data):
    total_points = 0
    total_credits = 0
    
    for item in subjects_data:
        total_points += (item['grade_point'] * item['credit'])
        total_credits += item['credit']
        
    if total_credits == 0:
        return 0.0, 0
        
    gpa = total_points / total_credits
    return gpa, total_credits