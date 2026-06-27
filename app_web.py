import streamlit as st
import pandas as pd
import os

# Import your existing logic
from grade_mapping import get_grade_point
from gpa_calculator import calculate_semester_gpa
from cgpa_calculator import calculate_cgpa
from pdf_generator import generate_pdf_report

# Page configuration
st.set_page_config(page_title="CGPA Calculator", layout="wide")

# --- BOLD TITLES, GREEN FOCUS & GREEN BUTTONS CSS ---
st.markdown("""
<style>
/* 1. Green Focus Border */
div[data-baseweb="input"]:focus-within, 
div[data-baseweb="input"] > div:focus-within, 
div[data-baseweb="select"]:focus-within, 
div[data-baseweb="select"] > div:focus-within {
    border-color: #2ecc71 !important;
    box-shadow: 0 0 4px #2ecc71 !important;
}

/* 2. Bold Titles */
.bold-title {
    font-weight: bold !important;
    font-size: 1.1rem;
    margin-bottom: 2px !important;
}

/* 3. Green Buttons */
div.stButton > button {
    background-color: #2ecc71 !important; 
    color: white !important; 
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'semester_records' not in st.session_state:
    st.session_state.semester_records = []

if 'direct_cred_input' not in st.session_state:
    st.session_state.direct_cred_input = 1.0

# --- Database Setup ---
@st.cache_data
def load_credits_db():
    builtin_db = {
        "Foundation English": 3, "Matrices And Calculus": 4, "Engineering Physics": 4,
        "Engineering Drawing And 3D Modelling": 4, "Engineering Chemistry": 4, 
        "Computer Programming In Python": 4, "Heritage Of Tamils": 1, "Ncc/Nss/Nso/Yrc": 0,
        "Professional Communication": 3, "Ordinary Differential Equations And Transform Techniques": 4,
        "Material Science": 3, "Basics Of Electrical And Electronics Engineering": 3,
        "Makerspace": 3, "Engineering Mechanics": 4, "Tamils And Technology": 1,
        "Audit Course I": 0, "Probability And Statistics": 4, "Work System Design": 4,
        "Manufacturing Processes": 4, "Fluid Mechanics And Machinery": 4, "Mechanics Of Materials": 4,
        "Industrial Standards For Industrial Engineering": 1, "Universal Human Values": 2,
        "Mechanics Of Machines": 3, "Thermodynamics": 3, "Applied Ergonomics": 4,
        "Operations Research": 4, "Manufacturing Automation": 4, "Design Thinking": 3,
        "Skill Development Course": 2, "Audit Course II": 0, "Production And Operations Management": 4,
        "Engineering Quality Control": 4, "Total Quality Management": 3, "Machine Design": 4,
        "Design Of Experiments": 4, "Reliability Engineering": 3, "Industry Oriented Course- I": 1,
        "Engineering Entrepreneurship Development": 3, "Capstone Design Project - Level I": 6,
        "Honours Elective - I": 3, "Honours Elective - II": 3, "Minor Elective - I": 3,
        "Minor Elective - II": 3, "Professional Elective Course- I": 3, "Professional Elective Course- II": 3,
        "Professional Elective Course- III": 3, "Professional Elective Course- IV": 3,
        "Emerging Technology Course I": 3, "Open Elective - I": 3, "Emerging Technology Course II": 3,
        "Self-Learning Course": 1, "Capstone Design Project - Level II": 6, "Applied Multivariate Analysis": 4,
        "Simulation Modelling And Analysis": 4, "Supply Chain Management": 4,
        "Perspective Of Sustainable Development": 3, "Project Work / Internship": 8
    }
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "database", "credits_datasheet.xlsx")
        if os.path.exists(filepath):
            df = pd.read_excel(filepath)
            excel_db = {str(row['Subject Name']).strip().title(): row['Credits'] for _, row in df.iterrows()}
            builtin_db.update(excel_db)
    except Exception: pass
    return builtin_db

credits_db = load_credits_db()
subject_list = ["Select Subject"] + sorted(list(credits_db.keys()))

# --- UI Layout ---
def main():
    st.title("🎓 B.E. Industrial Engineering CGPA Calculator")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Add Semester Data")
        
        st.markdown('<p class="bold-title">Semester Number</p>', unsafe_allow_html=True)
        sem_num = st.number_input("Semester Number", min_value=1, max_value=8, step=1, label_visibility="collapsed")
        
        st.markdown('<p class="bold-title">Entry Mode</p>', unsafe_allow_html=True)
        entry_mode = st.radio("Entry Mode", ["Calculate Subject-wise", "Direct GPA Entry"], horizontal=True, label_visibility="collapsed")
        
        if entry_mode == "Direct GPA Entry":
            st.markdown('<p class="bold-title">Enter GPA</p>', unsafe_allow_html=True)
            direct_gpa = st.number_input("Enter GPA", min_value=0.0, max_value=10.0, step=0.01, label_visibility="collapsed")
            
            st.markdown('<p class="bold-title">Total Credits</p>', unsafe_allow_html=True)
            direct_credits = st.number_input("Total Credits", min_value=1.0, max_value=40.0, step=0.5, key="direct_cred_input", label_visibility="collapsed")
            
            # --- Credit Calculator Popup (Expander) ---
            with st.expander("❓ Don't know the exact credits? Calculate them here"):
                st.write("Select subjects to auto-calculate the total credits.")
                calc_num_subjects = st.number_input("Number of subjects", min_value=1, max_value=12, value=5, key="calc_num")
                
                calc_total = 0.0
                
                c_man, c_sub, c_cred = st.columns([0.7, 3, 1])
                with c_man: st.markdown('<p class="bold-title">Type</p>', unsafe_allow_html=True)
                with c_sub: st.markdown('<p class="bold-title">Subject</p>', unsafe_allow_html=True)
                with c_cred: st.markdown('<p class="bold-title">Credits</p>', unsafe_allow_html=True)

                for i in range(calc_num_subjects):
                    c_man, c_sub, c_cred = st.columns([0.7, 3, 1])
                    
                    with c_man:
                        is_manual = st.toggle(" ", key=f"calc_man_{i}", help="Turn ON to type manually")
                    
                    with c_sub:
                        if is_manual:
                            calc_sub = st.text_input(f"Sub {i}", key=f"calc_sub_txt_{i}", label_visibility="collapsed", placeholder="Type subject name...")
                        else:
                            calc_sub = st.selectbox(f"Sub {i}", subject_list, key=f"calc_sub_sel_{i}", label_visibility="collapsed")

                    with c_cred:
                        calc_default = float(credits_db.get(calc_sub, 0.0)) if not is_manual and calc_sub in credits_db else 0.0
                        calc_cred = st.number_input(f"Cr {i}", min_value=0.0, max_value=10.0, value=calc_default, step=1.0, key=f"calc_cred_{i}_{calc_sub}", label_visibility="collapsed")
                        
                        if calc_sub != "Select Subject" and calc_sub.strip() != "":
                            calc_total += calc_cred
                
                st.markdown(f"### **Total Calculated Credits: {calc_total}**")
                
                def apply_calculated_credits(val):
                    st.session_state.direct_cred_input = val

                st.button("✅ Use this Total", type="primary", on_click=apply_calculated_credits, args=(calc_total,))

            st.write("") 
            if st.button("Save Semester (Direct)"):
                st.session_state.semester_records.append({
                    'sem': sem_num, 'gpa': direct_gpa, 'total_credits': direct_credits
                })
                st.success(f"Semester {sem_num} saved!")
                st.rerun()

        else:
            st.write("Select your subjects below:")
            
            st.markdown('<p class="bold-title">How many subjects?</p>', unsafe_allow_html=True)
            num_subjects = st.number_input("How many subjects?", min_value=1, max_value=12, value=5, label_visibility="collapsed")
            
            c_man, c_sub, c_cred, c_grade = st.columns([0.7, 3, 1, 1])
            with c_man: st.markdown('<p class="bold-title">Type</p>', unsafe_allow_html=True)
            with c_sub: st.markdown('<p class="bold-title">Subject Title</p>', unsafe_allow_html=True)
            with c_cred: st.markdown('<p class="bold-title">Credits</p>', unsafe_allow_html=True)
            with c_grade: st.markdown('<p class="bold-title">Grade</p>', unsafe_allow_html=True)

            subjects_data = []
            
            for i in range(num_subjects):
                c_man, c_sub, c_cred, c_grade = st.columns([0.7, 3, 1, 1])
                
                with c_man:
                    is_manual = st.toggle(" ", key=f"man_{i}", help="Turn ON to type manually")
                
                with c_sub:
                    if is_manual:
                        sub = st.text_input(f"Sub {i}", key=f"sub_txt_{i}", label_visibility="collapsed", placeholder="Type subject name...")
                    else:
                        sub = st.selectbox(f"Sub {i}", subject_list, key=f"sub_sel_{i}", label_visibility="collapsed")

                with c_cred:
                    default_cred = float(credits_db.get(sub, 0.0)) if not is_manual and sub in credits_db else 0.0
                    cred = st.number_input(f"Cr {i}", min_value=0.0, max_value=10.0, value=default_cred, step=1.0, key=f"cred_{i}_{sub}", label_visibility="collapsed")
                
                with c_grade:
                    grade = st.selectbox(f"Gr {i}", ["O", "A+", "A", "B+", "B", "C", "U"], key=f"grade_{i}", label_visibility="collapsed")
                
                if sub != "Select Subject" and sub.strip() != "" and cred > 0:
                    grade_point = get_grade_point(grade)
                    if grade_point is not None:
                        subjects_data.append({'subject': sub, 'credit': cred, 'grade_point': grade_point})

            st.write("") 
            if st.button("Calculate & Save Semester"):
                if subjects_data:
                    sem_gpa, sem_credits = calculate_semester_gpa(subjects_data)
                    st.session_state.semester_records.append({
                        'sem': sem_num, 'gpa': sem_gpa, 'total_credits': sem_credits
                    })
                    st.success(f"Semester {sem_num} saved! GPA: {sem_gpa:.3f}")
                    st.rerun()
                else:
                    st.warning("Please enter valid subjects and credits.")

    with col2:
        st.subheader("📊 Your Dashboard")
        
        if not st.session_state.semester_records:
            st.info("No data added yet.")
        else:
            for record in st.session_state.semester_records:
                st.markdown(f"**Sem {record['sem']}:** {record['gpa']:.3f} GPA *(Credits: {record['total_credits']})*")
            
            final_cgpa = calculate_cgpa(st.session_state.semester_records)
            st.metric(label="Current CGPA", value=f"{final_cgpa:.3f}")
            
            st.markdown("---")
            
            # --- PUTHUSA ADD PANNAPATTA CODE INGE THELIVA IRUKKU ---
            st.markdown("### 📝 Student Details for Report")
            student_name = st.text_input("Enter Your Name:")
            roll_number = st.text_input("Enter Your Roll Number:")
            
            # File save aagura idathoda path
            pdf_filename = "reports/Web_CGPA_Report.pdf"
            
            if st.button("Generate PDF Report"):
                # Rendu box-um empty-ah illama irukka nu theliva check pandrom
                if student_name.strip() and roll_number.strip(): 
                    
                    # session_state la irunthu correct-a data pass pandrom
                    success = generate_pdf_report(
                        st.session_state.semester_records, 
                        final_cgpa, 
                        student_name, 
                        roll_number,
                        pdf_filename
                    )
                    
                    if success and os.path.exists(pdf_filename):
                        st.success("✅ PDF Generated Successfully!")
                        
                        # Download button
                        with open(pdf_filename, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download PDF Now",
                                data=pdf_file,
                                file_name=f"{student_name}_CGPA_Report.pdf", # Pera veche download aagum
                                mime="application/pdf"
                            )
                    else:
                        st.error("Failed to generate PDF. Check terminal for details.")
                else:
                    st.warning("⚠️ Please enter both Name and Roll Number before generating the PDF.")
            
            st.write("")
            if st.button("Clear All Data"):
                st.session_state.semester_records = []
                st.rerun()

if __name__ == "__main__":
    main()