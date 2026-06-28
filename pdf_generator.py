import os
from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta

def generate_pdf_report(semester_records, final_cgpa, student_name, roll_number, filename="reports/Web_CGPA_Report.pdf"):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(base_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        filepath = os.path.join(base_dir, filename)
        chart_path = os.path.join(reports_dir, "gpa_chart.png")

        # --- 1. GENERATE THE GPA GRAPH ---
        semesters = [f"Sem {r['sem']}" for r in semester_records]
        gpas = [r['gpa'] for r in semester_records]

        plt.figure(figsize=(8, 4))
        plt.plot(semesters, gpas, marker='o', color='#1f6aa5', linestyle='-', linewidth=2.5, markersize=8)
        
        # Point mela values kaata
        for i, gpa_val in enumerate(gpas):
            plt.annotate(f"{gpa_val:.2f}", 
                         (semesters[i], gpas[i]), 
                         textcoords="offset points", 
                         xytext=(0, 8), 
                         ha='center', 
                         fontsize=10, 
                         fontweight='bold',
                         color='black')

        plt.title("Semester-wise GPA Trend", fontsize=14, fontweight='bold', color='#333333')
        plt.xlabel("Semesters", fontsize=12)
        plt.ylabel("GPA", fontsize=12)
        plt.ylim(0, 10.5) 
        plt.grid(True, linestyle='--', alpha=0.6)
        
        plt.savefig(chart_path, bbox_inches='tight', dpi=150)
        plt.close()

        # --- 2. GENERATE THE PDF REPORT ---
        pdf = FPDF()
        pdf.add_page()
        
        # Date and Time top right la
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        current_time = datetime.now(ist_timezone).strftime("%d-%m-%Y %I:%M %p") 

        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, txt=f"Date & Time: {current_time}", ln=True, align='R')
        
        # Title
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, txt="Department Of Industrial Engineering, CEG - AU", ln=True, align='C')
        pdf.cell(0, 10, txt="Academic Performance Report", ln=True, align='C')
        pdf.ln(5)
        
        # Add Student Name and Roll Number (Puthusa add pannathu)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, txt=f"Student Name : {student_name}", ln=True)
        pdf.cell(0, 8, txt=f"Roll Number  : {roll_number}", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Oru line podurathu kaga
        pdf.ln(5)

        # Text Data
        pdf.set_font("Arial", '', 12)
        for record in semester_records:
            pdf.cell(0, 10, txt=f"Semester {record['sem']} GPA: {record['gpa']:.3f}  (Total Credits: {record['total_credits']})", ln=True)
            
        pdf.ln(5)
        
        # Final CGPA
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=f"Current CGPA: {final_cgpa:.3f}", ln=True)
        pdf.ln(10)

        # Insert the Graph Image into the PDF
        if os.path.exists(chart_path):
            pdf.image(chart_path, x=15, y=pdf.get_y(), w=180)

        # Save the file
        pdf.output(filepath)
        print(f"[SUCCESS] PDF generated at {filepath}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate PDF: {e}")
        return False