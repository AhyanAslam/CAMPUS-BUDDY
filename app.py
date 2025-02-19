from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)  #initializing flask
app.secret_key = "supersecretkey"  #requirement for using flash

USER_DATA_FILE="users.json"  # file for storing users id password 

# Load users from file
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save users to file
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

# rendered home page
@app.route('/home')
def home():
    return render_template('index.html')

# rendered login page, checking user id and password
@app.route('/signin', methods=["GET","POST"])
def signin():
    if request.method == "POST":
        user_id = request.form["userid"]  # Get user ID from the form
        password = request.form["password"]  # Get password from the form
        users = load_users()  # Load existing users

        if user_id in users and users[user_id] == password:
            return redirect(url_for('home')) # after checking correct id password open home page
        else:
            flash("Invalid User ID or Password.")  # if any input is incorrect this message will show on the page

    return render_template("login.html") 

# rendered register page, 
@app.route('/register', methods=["GET", "POST"])
def register():
    # getting the information
    if request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        users = load_users()

        # Check if the user ID already exists
        if user_id in users:
            flash("User ID already exists.")
        else:
            # Save new user
            users[user_id] = password
            save_users(users)
            flash("Registration successful! You can now log in.")
            return redirect(url_for('register'))
    return render_template("register.html")
    
if __name__ == '__main__':
    app.run(debug=True)