def calculate_cgpa(semester_records):
    total_weighted_gpa = 0
    cumulative_credits = 0
    
    for record in semester_records:
        total_weighted_gpa += (record['gpa'] * record['total_credits'])
        cumulative_credits += record['total_credits']
        
    if cumulative_credits == 0:
        return 0.0
        
    return total_weighted_gpa / cumulative_credits