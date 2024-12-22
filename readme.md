# Flask User Management System

This project is a Flask-based user management system that supports registration, login, profile picture uploads, and password recovery. The application stores user data in a JSON file and displays user information dynamically on a welcome page.

## Features

- **User Registration**: Users can register with a username, password, phone number, and profile picture.
- **User Login**: Supports login with username or phone number.
- **Profile Picture Upload**: Users can upload profile pictures in `.png`, `.jpg`, `.jpeg`, or `.gif` formats.
- **Password Reset**: Users can reset their password if they forget it.
- **Session Management**: Tracks user login sessions and allows users to log out.
- **Error Handling**: Custom 404 error page for invalid routes.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7 or later
- Pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/flask-user-management.git
   cd flask-user-management
