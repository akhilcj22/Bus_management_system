
# 🚌 Bus Route Management System

This project is a **Bus Route Management System** developed as part of a mini-project for the **Bachelor of Technology** at **APJ Abdul Kalam Technological University**.

## 📋 Project Overview
In today's world, efficient transportation systems are crucial. The Bus Route Management System aims to improve the bus transportation experience by providing:
- Real-time bus search based on destinations
- Easy registration and login for users and bus owners
- Bus timing management by owners
- Feedback submission for service improvement
- Password recovery options for users

Built using **Flask (Python)** and **SQLite3**, this web application focuses on making the public bus system more accessible, efficient, and user-friendly.

## 🚀 Features
- **User Registration & Login**: Secure login and registration system for passengers.
- **Owner Registration & Dashboard**: Special login and dashboard for bus owners to update/manage bus timings.
- **Password Reset**: Secure password reset system with hashed password storage.
- **Bus Search Functionality**: Users can search buses by destination.
- **Owner Dashboard**: Bus owners can view and manage bus schedules.
- **Feedback System**: Passengers can submit feedback to improve services.
- **Real-Time Updates**: Users get updated timings based on the latest database entries.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (via Flask templates)

## 📂 Project Structure
```
/templates/      # HTML files like index.html, register.html, search.html, etc.
static/           # (optional) Static assets like CSS, JS, images
database.db       # User database
owner_database.db # Owner database
bus_timings.db    # Bus timings database
app.py            # Main Flask application
```

## 🔥 How to Run
1. Clone this repository.
2. Install Flask if not already installed:
   ```bash
   pip install flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and visit:  
   `http://127.0.0.1:5000/`

## 👨‍💻 Team Members
- **Akhil C J (VML21CS028)**
- **Santhipriya (VML21CS152)**
- **Anagha Nagesh (VML21CS051)**
- **Anandhu K P (VML21CS052)**

## 📜 Project Guide
- **Ms. Tintu Devasia** — Assistant Professor

Vimal Jyothi Engineering College, Chemperi
