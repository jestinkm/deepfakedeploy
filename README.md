# Deepfake Facial Recognition Project

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)  
[Live Frontend](https://darling-bombolone-94d5b1.netlify.app) | [GitHub Repository](https://github.com/jestinkm/deepfake) | [live viedo of working](https://drive.google.com/file/d/1c0-wRMEXkCyUuUw-IB0Z6yShS1RD7Wk3/view?usp=sharing)

---

## **Table of Contents**

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Folder Structure](#folder-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Deployment](#deployment)  
7. [Technologies Used](#technologies-used)  
8. [Future Enhancements](#future-enhancements)  
9. [License](#license)  

---

## **Project Overview**

This project is a **Deepfake/Facial Recognition secured file system** that:  

- Detects faces in real-time using webcam input  
- Shows private files only to authorized users  
- Closes files automatically if face is not detected  
- Supports threat analysis for anomalous behavior detection  

The system is split into:  

- **Frontend:** Static HTML/CSS/JS hosted on **Netlify**  
- **Backend:** Flask API for real-time facial recognition and file management  

---

## **Features**

- Real-time face recognition using OpenCV & face_recognition  
- Deepfake detection (future upgrade possible)  
- Automatic file access control: Opens/closes files based on face detection  
- Threat analysis: Detects anomalies in access attempts  
- Lightweight deployment: Frontend on Netlify, backend on free Python hosting (Replit/Railway)  
- Option to download project files directly from Google Drive  

---

## **Folder Structure**
deepfake/
│-- app.py # Flask backend
│-- requirements.txt # Python dependencies
│-- templates/ # HTML frontend
│ │-- index.html
│ │-- login.html
│ │-- signup.html
│-- static/ # CSS, JS, images
│ │-- style.css
│ │-- script.js
│-- README.md # This file
│-- venv310/ # Virtual environment (ignore in Git)


---

## **Installation (Local Setup)**

1. Clone the repository:
```bash
git clone https://github.com/jestinkm/deepfake.git
cd deepfake

Create a virtual environment:

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

Usage (Local)

Run the Flask server:

python app.py


Open your browser at:

http://127.0.0.1:5000/


Login and test facial recognition features.

Optional: Download full project files from Google Drive:
Download Link

Deployment (Free)
Frontend (Netlify)

Base directory: .

Publish directory: templates

Build command: (leave empty)

Backend (Flask API)

Deploy on Replit or Railway free tier

Flask must listen on 0.0.0.0 and port=int(os.environ.get("PORT", 5000))

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

Technologies Used

Frontend: HTML, CSS, JavaScript

Backend: Python, Flask, Flask-CORS

Face Detection: OpenCV, Mediapipe / face_recognition

Package Management: pip, requirements.txt

Deployment: Netlify (frontend), Replit/Railway (backend)

Future Enhancements

GPU-based deepfake detection

User authentication and roles

Cloud storage for private files (AWS S3/Firebase)

Real-time alerts on anomaly detection

License

MIT License — see LICENSE

Git Push Instructions
# 1. Check status
git status

# 2. Add all files (except venv)
git add .

# 3. Commit with a message
git commit -m "Initial commit - Deepfake project"

# 4. Set remote if not already set
git remote add origin https://github.com/jestinkm/deepfake.git

# 5. Push to main branch
git push -u origin main


⚠️ Make sure to ignore your virtual environment (venv310) by adding it to .gitignore:

venv310/
__pycache__/
*.pyc



