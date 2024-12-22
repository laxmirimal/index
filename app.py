from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# File to store user data
USER_DATA_FILE = 'users.json'

# Folder to store uploaded profile pictures
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load user data from file
def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    logged_in = 'username' in session
    return render_template('index.html', logged_in=logged_in, username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phonenumber = request.form['number']
        photo = request.files['photo']

        users = load_users()

        # Check if the username already exists
        if username in users:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Handle file upload
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
        else:
            flash('Invalid file type. Allowed types are png, jpg, jpeg, gif.', 'error')
            return redirect(url_for('register'))

        # Save user data (username, password, phone number, and photo filename)
        users[username] = {
            'password': password,
            'phone': phonenumber,
            'photo': filename
        }
        save_users(users)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        login_input = request.form['username']  # Input can be username or phone
        password = request.form['password']
        users = load_users()

        # Check if input matches username or phone number
        for username, details in users.items():
            if (login_input == username or login_input == details.get('phone')) and details['password'] == password:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('welcome'))

        flash('Invalid username/phone number or password. Please try again.', 'error')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

    users = load_users()
    username = session['username']
    photo_filename = users[username].get('photo', 'default.png')  # Default photo if none exists
    photo_url = url_for('static', filename=f'uploads/{photo_filename}')

    return render_template('welcome.html', username=username, photo_url=photo_url)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        try:
            
            identifier = request.form['identifier']  # Can be username or phone number
            new_password = request.form['new_password']
        except KeyError as e:
            flash('Missing form data. Please fill out all fields.', 'error')
            return redirect(url_for('forgot_password'))

        users = load_users()

        # Find the user by username or phone number
        user_to_update = None
        for username, details in users.items():
            if username == identifier or details.get('number') == identifier:
                user_to_update = username
                break

        if user_to_update:
            # Update the user's password
            users[user_to_update]['password'] = new_password
            save_users(users)
            flash('Password reset successful. Please log in with your new password.', 'success')
            return redirect(url_for('login'))

        flash('User not found. Please register first.', 'error')
        return redirect(url_for('register'))

    return render_template('forgot_password.html')




@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
