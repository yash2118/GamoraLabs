# GamoraLabs — AI Academic Assistant & Mentor-Mentee Platform
## Project Overview
GamoraLabs is an AI-powered academic support platform. The platform helps students access academic information using natural language queries while also enabling peer-to-peer mentorship through a Mentor-Mentee matching system. Students can ask questions related to:
- Courses
- Professors
- Grades
- Room schedules
using an AI-powered assistant connected to university data.
## Why This Project?
Students often need to navigate multiple university portals to access academic information, making the process inefficient and time-consuming. This project was built to:
- Simplify access to academic resources
- Provide AI-powered student assistance
- Encourage collaborative learning through mentorship
It combines AI, database systems, real-time APIs, and secure authentication into a single student-focused platform.
## Problem Statement
Students commonly face:
- Difficulty accessing academic information quickly
- fragmented university systems
- Limited peer academic support
GamoraLabs solves this by creating a centralized AI academic assistant, a mentor-mentee platform for easier academic guidance and collaboration.
## Key Features
### AI Academic Assistant
- Uses Gemini 1.5 Pro to convert natural language into SQL queries
- Retrieves real-time academic data through Nebula API
- Supports queries related to courses, grades, professors, and room schedules
### Mentor-Mentee Platform
- Students can register as mentors
- Share expertise and availability
- Allow mentees to schedule academic guidance sessions
### Security & Authentication
- bcrypt password hashing for secure authentication
- SQL injection protection for safe query execution
### Interactive Frontend
- Built with Streamlit for a simple and responsive user experience
## Workflow
User Query -> Gemini 1.5 Pro -> Natural Language → SQL -> Query Validation -> Nebula API / MySQL -> Results Displayed in Streamlit
## Impact & Use Cases
### Students
- Faster access to academic information
- Easier course and professor lookup
- Peer mentorship opportunities
### Universities
- Improved student engagement
- Centralized academic support system
### Mentors & Mentees
- Better academic collaboration
- Personalized student guidance
## Technologies Used
| Category       | Technologies   |
| -------------- | -------------- |
| Frontend       | Streamlit      |
| Backend        | MySQL          |
| AI Integration | Gemini 1.5 Pro |
| Programming    | Python         |
| Data Handling  | Pandas         |
| Authentication | bcrypt         |

## Conclusion
GamoraLabs demonstrates how AI-powered systems can improve the student experience by simplifying access to academic information and enabling collaborative learning through mentorship. The project combines:
- LLM-powered querying
- Secure database interaction
- Peer mentorship
into a unified academic support platform.
