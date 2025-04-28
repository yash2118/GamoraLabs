# GamoraLabs
Gamora Labs - AI Academic Assistant and Mentor-Mentee Platform
🚀 Built at HackAI 2025 | Challenge by Nebula Labs (UT Dallas)

Gamora Labs is an AI-powered academic support platform designed to enhance the student experience at UT Dallas.
It features an intelligent assistant that allows students to ask natural language questions about courses, professors, grades, and room schedules, along with a peer-to-peer Mentor-Mentee matching system for academic support.

# ✨ Key Features
## AI Academic Assistant:
Leveraged Google's Gemini 1.5 Pro LLM to translate natural language queries into SQL.
Accessed real-time academic data via Nebula Labs' Nebula API (CourseBook, Grades, Room Scheduling, Profiles).

## Mentor-Mentee Matching Platform:
Students can register as mentors, share expertise, set availability, and allow mentees to schedule guidance sessions.

## Secure Authentication:
User data and login credentials protected using bcrypt hashing.

## Safe Query Execution:
AI outputs validated and protected against SQL injection to maintain database security.

## Streamlit Frontend:
Simple, interactive, and mobile-responsive UI for students to easily interact with the system.

# 🛠 Tech Stack
Frontend/UI: Streamlit
Backend: MySQL
AI Integration: Gemini 1.5 Pro (LLM API)
Data Handling: Python, Pandas
Authentication: bcrypt
Security: SQL Injection Protection

## 🚀 Getting Started
Clone the repository:
git clone https:[//github.com/yourusername/GamoraLabs.git](https://github.com/yash2118/GamoraLabs)

Set up a virtual environment and install dependencies:
pip install -r requirements.txt

Configure your environment variables:
Nebula API credentials
Gemini API key

MySQL Database URL
Run the Streamlit app:
streamlit run app.py
