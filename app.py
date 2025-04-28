import streamlit as st
import mysql.connector
import pandas as pd
import google.generativeai as genai
import re
import bcrypt

# --- Configuration ---
genai.configure(api_key="AIzaSyDf5OVlcDYq6ZTO5bSlX_juje8EvE1rvVI")  # 🔐 Replace with your Gemini API key
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "insight_database"
}
model = genai.GenerativeModel('gemini-1.5-pro', generation_config={"temperature": 0.3})
status_icons = {"available": "🟢", "busy": "🔴", "afk": "🟡", "done": "⚫"}

# --- Helper Functions ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def enforce_distinct(sql: str) -> str:
    pattern = re.compile(r"select\s+", re.IGNORECASE)
    if pattern.search(sql) and "distinct" not in sql.lower():
        return pattern.sub("SELECT DISTINCT ", sql, count=1)
    return sql

def generate_sql(question: str) -> str:
    schema = """
    Tables:
    - mentors (name, utd_email, skill, availability_day, availability_time, status)
    - professors (id, first_name, last_name, email)
    - courses (course_id, title, class_level)
    - grades (professor_id, course_id, section_id, A, Aminus, Bplus, B, Bminus, Cplus, C, Cminus, Dplus, D, Dminus, F, W)
    """
    prompt = f"""
                You are a SQL query generator. You generate concise queries with DISTINCT keyword for the provided prompt, without any code blocks or markdown formatting.
                If the prompt isn't related to getting a SQL query, return 'INVALID'.
                Course ID is of format <title><class_level> e.g., CS1234.

                Schema:{schema}
                professors (id, first_name, last_name, email, phone_number) Key(id)
                courses (course_id, title, class_level) Key(course_id)
                grades (professor_id, course_id, section_id, A, Aminus, Bplus, B, Bminus, Cplus, C, Cminus, Dplus, D, Dminus, F, W) Key(professor_id, course_id, section_id)
                mentors (full_name, email, skills, availability_day, availability_time) Key(email)

                User queries you should be able to convert:

                Who are all the professors in the system?
                List the email addresses of all professors.
                Which professors have phone numbers starting with 972?
                Show me all professors whose first name is John.
                Which professors do not have an email listed?
                What are all the available courses?
                List courses where the class level is 4000.
                Which courses have “Data” in their title?
                Show me courses titled "Machine Learning."
                What are the course IDs for Artificial Intelligence classes?
                Which professor gave the most A grades?
                List professors with the highest number of W grades.
                How many students received F in CS1337?
                Show grade distribution for CS3305.
                Who gave the highest number of Cminus grades?
                What professors taught CS1337?
                List professor names along with the course titles they taught.
                Show professor emails who taught a 3000 level course.
                For each professor, show total A and B grades given.
                Which professor gave the most A grades for CS2305?
                Who is available to mentor Python on Monday?
                List mentors who are free at 2pm.
                Show all mentors available on Friday afternoon.
                Which mentors have SQL and Python both listed in their skills?
                Find mentors available on Saturday with “Machine Learning” skill.
                What courses have been taught by professors whose email ends with utd.edu?
                Who gave the highest number of Bplus grades for CS1337?
                List all professors who taught more than one course.
                Who has given a total of more than 20 F grades across all sections?
                List mentors who can help with resume writing and are available after 3pm."""
    try:
        response = model.generate_content(prompt + "\nQ: " + question)
        sql_match = re.search(r"SELECT\s.+?FROM\s.+?(WHERE\s.+?)?;", response.text, re.IGNORECASE | re.DOTALL)
        if sql_match:
            clean_sql = enforce_distinct(sql_match.group(0).replace("`", "").strip())
            if any(cmd in clean_sql.upper() for cmd in ["INSERT", "UPDATE", "DELETE", "DROP"]):
                return "INVALID"
            return clean_sql
        return "INVALID"
    except Exception as e:
        st.error(f"Gemini Error: {str(e)}")
        return "INVALID"

def run_query(sql: str) -> pd.DataFrame:
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return pd.DataFrame()

# --- Streamlit UI ---
st.set_page_config(page_title="UTD Academic System", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎓 UTD Academic + Mentor Assistant</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📚 Academic Query", "🤝 Mentor Booking", "🔐 Mentor Portal"])

# === 📚 Academic Query Tab ===
with tab1:
    st.markdown("### 💬 Ask a question about professors, courses, or grades:")
    question = st.text_input("Example: Who gave the most A grades in CS1337?")

    if st.button("🧠 Generate SQL & Fetch Data"):
        with st.spinner("Thinking..."):
            sql = generate_sql(question)
            if sql == "INVALID":
                st.error("Gemini couldn't generate a valid SQL query.")
            else:
                st.code(sql, language="sql")
                df = run_query(sql)
                if not df.empty:
                    st.dataframe(df)
                    summary = model.generate_content(f"Summarize: {question}\nData: {df.head(3).to_string()}").text
                    st.success(summary)
                else:
                    st.warning("No results found for this query.")

    with st.expander("💡 Query Examples"):
        st.markdown("Try things like:\n- Who teaches CS1337?\n- What are all 4000-level courses?\n- Show mentors for Python.")

# === 🤝 Mentor Booking Tab ===
with tab2:
    st.markdown("### 👨‍🏫 Book a Mentor Session")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mentors WHERE status = 'available'")
    mentors = cursor.fetchall()

    available_days = sorted(set(m['availability_day'].strip() for m in mentors if m['availability_day']))
    available_times = sorted(set(m['availability_time'].strip() for m in mentors if m['availability_time']))

    for mentor in mentors:
        with st.container():
            st.markdown(f"""
            {status_icons[mentor['status'].lower()]} {mentor['name']}  
            - 🛠 Skill: {mentor['skill']}  
            - 📅 Availability: {mentor['availability_day']} {mentor['availability_time']}  
            - 📧 [{mentor['utd_email']}](mailto:{mentor['utd_email']})
            """)

    with st.form("booking"):
        st.markdown("#### 📝 Book a Session")
        mentee_name = st.text_input("Your Name")
        mentor_names = [m['name'] for m in mentors]
        selected_mentor = st.selectbox("Choose a Mentor", mentor_names)
        col1, col2 = st.columns(2)
        with col1:
            requested_day = st.selectbox("Preferred Day", available_days)
        with col2:
            requested_time = st.text_input("Preferred Time (e.g. 2-4 PM)")

        if st.form_submit_button("📅 Book Now"):
            cursor.execute("SELECT * FROM mentors WHERE name = %s", (selected_mentor,))
            mentor = cursor.fetchone()
            if mentor and requested_day.lower() == mentor['availability_day'].lower() and requested_time.lower() == mentor['availability_time'].lower():
                slot = f"{requested_day} {requested_time}"
                cursor.execute("SELECT * FROM mentor_bookings WHERE mentor_id = %s AND slot = %s AND status = 'pending'", (mentor['id'], slot))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO mentor_bookings (mentor_id, mentee_name, slot) VALUES (%s, %s, %s)", (mentor['id'], mentee_name, slot))
                    cursor.execute("UPDATE mentors SET status = 'busy' WHERE id = %s", (mentor['id'],))
                    conn.commit()
                    st.success("✅ Booking confirmed!")
                else:
                    st.error("⛔ Slot already booked.")
            else:
                st.error("⛔ Mentor is not available at that time.")
    cursor.close()
    conn.close()

# === 🔐 Mentor Portal ===
with tab3:
    st.markdown("### 🔐 Mentor Login & Profile")

    if "mentor" not in st.session_state:
        with st.form("login"):
            email = st.text_input("UTD Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("🔓 Login"):
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM mentors WHERE utd_email = %s", (email,))
                mentor = cur.fetchone()
                cur.close()
                conn.close()
                if mentor and verify_password(mentor['password_hash'], password):
                    st.session_state.mentor = mentor
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")

    elif "mentor" in st.session_state:
        mentor = st.session_state.mentor
        st.success(f"Welcome, {mentor['name']}!")
        with st.form("update_status"):
            col1, col2 = st.columns(2)
            with col1:
                day = st.selectbox("Available Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(mentor['availability_day']))
            with col2:
                time = st.text_input("Time Slot", value=mentor['availability_time'])
            status = st.selectbox("Status", list(status_icons.keys()), index=list(status_icons.keys()).index(mentor['status']))
            if st.form_submit_button("Update Availability"):
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("UPDATE mentors SET availability_day = %s, availability_time = %s, status = %s WHERE id = %s", (day, time, status, mentor['id']))
                conn.commit()
                cur.close()
                conn.close()
                st.success("Updated successfully!")
                st.balloons()

        if st.button("🚪 Logout"):
            del st.session_state["mentor"]
            st.rerun()

    with st.expander("📝 Register as a New Mentor"):
        with st.form("register"):
            name = st.text_input("Name*")
            utd_email = st.text_input("UTD Email*")
            skill = st.text_input("Skills* (comma-separated)")
            day = st.selectbox("Available Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            time = st.text_input("Available Time (e.g. 2-4 PM)")
            pw = st.text_input("Password*", type="password")
            confirm_pw = st.text_input("Confirm Password*", type="password")
            if st.form_submit_button("Register"):
                errors = []
                if not all([name, utd_email, skill, day, time, pw, confirm_pw]):
                    errors.append("All fields are required.")
                if "@utdallas.edu" not in utd_email:
                    errors.append("Must use UTD email.")
                if pw != confirm_pw:
                    errors.append("Passwords do not match.")
                if len(pw) < 8:
                    errors.append("Password too short.")
                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    try:
                        conn = mysql.connector.connect(**DB_CONFIG)
                        cur = conn.cursor()
                        hashed = hash_password(pw)
                        cur.execute("INSERT INTO mentors (name, utd_email, skill, availability_day, availability_time, password_hash, status) VALUES (%s, %s, %s, %s, %s, %s, 'available')", (name.strip(), utd_email.strip().lower(), skill.strip(), day.strip(), time.strip(), hashed))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success("Registration successful! You can now log in.")
                    except mysql.connector.IntegrityError:
                        st.error("Email already registered.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")