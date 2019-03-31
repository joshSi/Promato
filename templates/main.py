import firebase
from flask import Flask, request, render_template, redirect
from config import config #config.py is a dictionary containing
app = Flask(__name__)

firebase = firebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
user = False

@app.route("/", methods = ['GET', 'POST'])
def splash():
    return "HOMEPAGE"

@app.route("/login", methods = ['GET', 'POST'])
def login():
    global user
    invalid = 'Login invalid, please check your credentials.'
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pass']
        try: 
            user = auth.sign_in_with_email_and_password(email, password)
            return redirect('/home') #after login
        except:
            return render_template('login.html', fail = invalid)
    return render_template('login.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    global user
    invalid = 'Something went wrong with registration, please try again.'
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pass']
        name = request.form['user_name']
        try:
            user = auth.create_user_with_email_and_password(email, password, name)
            return redirect('/home')
        except:
            return render_template('register.html', fail = invalid)
    return render_template('register.html')

@app.route("/home")
def home():
    global user
    if user == False:
        return redirect('/')
    return render_template('home.html', welcome_name = user['displayName'])

@app.route("/setup", methods = ['GET', 'POST'])
def setup():
    global user
    if user == False:
        return redirect('/')
    if request.method == 'POST':
        data = {"cycles": request.form['user_task'],
            "task": request.form['user_task']}
        results = db.child("users").child(user['displayName']).push(data)
        return render_template('setup.html')
    return render_template('setup.html')

@app.route("/timer", methods = ['GET', 'POST'])
def time():
    if user == False:
        return redirect('/')
    return render_template('setup.html')

if __name__ == "__main__":
    app.run(debug = True)