# Flask-Individual-Project: Online Absence Catalog Application

This application is an **online catalog for student absences**, where students can view their total and individual absences by date and reason, while professors can enter absences for their students. The admin has full control over the application and can visualize statistical graphs about student absences, including per-discipline charts.

## Technologies Used

This application is built using **Flask**, a Python micro-framework that allows for the rapid development of web applications. A combination of libraries and technologies were used to create a functional and secure application.

### Framework and Libraries
- **Flask**: The micro-framework for Python used to build the web application.
- **Flask-SQLAlchemy**: Used for interacting with the database via ORM (Object-Relational Mapping), managing data storage.
- **SQLAlchemy**: Used for managing relational databases (PostgreSQL).
- **Matplotlib**: Used for creating graphical visualizations of student absences per discipline.
- **PostgreSQL**: Used for storing and managing data related to students, professors, and absences.

## Features
- **Authentication**: Users (students and professors) can log in with their email address. Passwords are securely stored.
- **Absence Management**: Professors can enter absences for students on specific dates for their courses, and admins can generate and view statistical graphs for absences per discipline.
- **Statistical Visualization**: Admins can view a graph about absences for each discipline, generated automatically using Python and the Matplotlib library.
- **CRUD Operations**: Admins can create, edit, and delete accounts for professors and students.
- **Security**: All sensitive data is securely stored. The application uses strong encryption to ensure data protection.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL installed on your system

### Install Dependencies

Clone this repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/username/repository.git
cd repository
pip install -r requirements.txt
