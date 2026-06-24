import os
from fpdf import FPDF
import matplotlib.pyplot as plt

def generate_pdf_report(semester_records, final_cgpa, filename="reports/CGPA_Report.pdf"):
    try:
        # Guarantee the app finds the correct folder to save the PDF
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(base_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        filepath = os.path.join(base_dir, filename)
        chart_path = os.path.join(reports_dir, "gpa_chart.png")

        # --- 1. GENERATE THE GPA GRAPH ---
        semesters = [f"Sem {r['sem']}" for r in semester_records]
        gpas = [r['gpa'] for r in semester_records]

        # Create a beautiful graph
        plt.figure(figsize=(8, 4))
        plt.plot(semesters, gpas, marker='o', color='#1f6aa5', linestyle='-', linewidth=2.5, markersize=8)
        
        plt.title("Semester-wise GPA Trend", fontsize=14, fontweight='bold', color='#333333')
        plt.xlabel("Semesters", fontsize=12)
        plt.ylabel("GPA", fontsize=12)
        plt.ylim(0, 10.5) # Keep the Y-axis fixed from 0 to 10
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Save the graph as an image in the reports folder
        plt.savefig(chart_path, bbox_inches='tight', dpi=150)
        plt.close()

        # --- 2. GENERATE THE PDF REPORT ---
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(200, 10, txt="Academic Performance Report", ln=True, align='C')
        pdf.ln(10)
        
        # Text Data
        pdf.set_font("Arial", '', 12)
        for record in semester_records:
            pdf.cell(200, 10, txt=f"Semester {record['sem']} GPA: {record['gpa']:.3f}  (Total Credits: {record['total_credits']})", ln=True)
            
        pdf.ln(5)
        
        # Final CGPA
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Current CGPA: {final_cgpa:.3f}", ln=True)
        pdf.ln(10)

        # Insert the Graph Image into the PDF
        if os.path.exists(chart_path):
            pdf.image(chart_path, x=15, y=None, w=180)

        # Save the file
        pdf.output(filepath)
        print(f"[SUCCESS] PDF generated at {filepath}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate PDF: {e}")
        return False