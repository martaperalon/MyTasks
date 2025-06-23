# MyTasks – Task Management Web App

#### Video Demo: https://youtu.be/pqTRXrEXI7o

**Author:** Marta Pérez Alonso
**GitHub:** martaperalon
**edX:** martaperalon
**Date:** June 21, 2025

---

## Description

MyTasks is a web-based task management application that stands out for its minimalist design and simple functionality. It is designed for users who want a clear, distraction-free tool to jot down pending tasks, mark them as completed, and delete them when no longer needed.

The app allows each user to manage their own personal task list after registering and logging in. Although it lacks advanced features like subtasks, automatic reminders, or complex filters, its strength lies precisely in its ease of use. Each task can optionally include a date, but this is not mandatory and no complex tracking is involved.

This project was developed as the final work for the **CS50’s Introduction to Computer Science** course, aiming to practice fundamental concepts such as user authentication, session management, data persistence with databases, and responsive web design. The priority was always to maintain a clean, understandable, and accessible interface for users of all levels.

---

## Features

The main functionalities of MyTasks include:

- **User authentication:** registration, login, and logout, with passwords securely hashed using Werkzeug.
- **Personalized dashboard:** each user accesses their own space where they can see only their tasks.
- **Task creation and deletion:** intuitive interface to add new tasks or delete them when no longer needed.
- **Mark tasks as completed:** helps visualize progress and keep the list clean.
- **Persistent storage:** data is securely stored in a SQLite database.

These features make MyTasks a versatile tool for both personal and professional use.

---

## Project Structure

The project has the following directory structure:
```
/project/
├── static/
│ └── style.css # Custom styles
├── templates/ # HTML templates (Jinja2)
│ ├── layout.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
├── app.py # Main application logic (Flask)
├── README.md
└── tasks.db # SQLite database
```

The code organization clearly separates backend logic, frontend presentation, and data persistence, which facilitates maintenance and scalability.

---

## Technologies Used

During the development of MyTasks, I used the following technologies:

- **Python 3 + Flask:** web framework to manage routes, sessions, and server logic.
- **SQLite:** lightweight database, ideal for small projects and prototypes.
- **Jinja2:** templating engine for generating dynamic HTML.
- **Werkzeug:** library used for secure password hashing.

These tools complement each other well and are perfect for a project of this scale. Additionally, their extensive documentation greatly facilitated the learning process.

---

## Design Decisions

From the beginning, I made several key design decisions:

- **Minimalist interface:** I opted for a clean design that avoids distractions, favoring productivity.
- **Separation of concerns:** the architecture clearly distinguishes between business logic (Flask), presentation (HTML + CSS), and data (SQLite).
- **Security as a priority:** passwords are never stored in plaintext, and access to tasks is fully isolated per user.
- **Preparedness for future expansions:** the code is designed to allow easy addition of new features such as recurring tasks, email reminders, or tagging.

One of the most important decisions was implementing user session control and limiting data access. This required careful attention to data flow and designing protected routes.

---

## How to Run Locally

To run MyTasks on your local machine:

```
cd project
flask run
```
## Lessons Learned
This project was an excellent opportunity to apply fundamental CS50 concepts. I learned to integrate Flask with a database and manage routes and sessions securely. I also strengthened my web interface design skills.

One of the most interesting challenges was ensuring that each user could only see their own tasks. This helped me better understand how Flask sessions work and how to apply proper filtering in database queries.

Furthermore, I realized the importance of designing code with future extensions in mind. Structuring the project modularly makes it easier to add new features without having to rewrite large parts of the existing code.

## Credits
This project was developed as the final assignment for the CS50x course (2025). I am grateful to the entire Harvard team and the CS50 community for the resources, challenges, and constant support during the course. I also thank the Flask and SQLite official documentation and forums for being key tools in successfully developing this application.

