ShivShiksha - Virtual Classroom Platform
ShivShiksha is a virtual classroom web application built using Flask (Python) and deployed on AWS infrastructure. It offers an easy-to-use platform for students, instructors, and admins to manage learning online. Designed to promote free education and empower learners, this system supports user registration, course management, and real-time access to resources.

🔧 Tech Stack
Frontend: HTML5, CSS3, Bootstrap 5

Backend: Python (Flask)

Database: MySQL (via XAMPP in local development)

Deployment: AWS (S3, EC2, RDS planned)

Email Functionality: PHPMailer or SMTP (configurable)

✨ Features
User roles: Student, Instructor, Admin

Secure login/register system

Course listing and detail pages

Modern responsive UI

Simple and clean navigation

Free access to learning materials


📁 Project Structure
shiv-shiksha/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── app.py
├── config.py
├── requirements.txt
└── README.md



🚀 Getting Started (Local)
Clone the repo:

bash
Copy
Edit
git clone https://github.com/Vishal3762/shiv-shiksha.git
cd shiv-shiksha
Set up a virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Start XAMPP and run MySQL.

Import the SQL file in phpMyAdmin.

Run the Flask app:

bash
Copy
Edit
python app.py
Open browser and go to http://127.0.0.1:5000

