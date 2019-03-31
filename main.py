import fyrebase
from flask import Flask, request, render_template, redirect
from config import config #config.py is a dictionary containing
app = Flask(__name__)

firebase = fyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
user = False
work_timer = 10
rest_timer = 5
@app.route("/", methods = ['GET', 'POST'])
def splash():
    return render_template('splash.html')

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

@app.route("/home", methods = ['GET', 'POST'])
def home():
    global user
    if user == False:
        return redirect('/')
    return render_template('home.html', welcome_name = user['displayName'])

@app.route("/setup", methods = ['GET', 'POST'])
def setup():
    global user
    global pomo_count
    if user == False:
        return redirect('/')
    if request.method == 'POST':
        pomo_count = int(request.form['pomodoro_count'])
        data = {"cycles": pomo_count,
            "task": request.form['user_task']}
        results = db.child("users").child(user['displayName']).push(data)
        return redirect('/timer')
    return render_template('setup.html')

@app.route("/timer", methods = ['GET', 'POST'])
def time():
    global work_timer
    global pomo_count

    work_timer -= 1
    if user == False:
        return redirect('/')
    if work_timer <= 0:
        pomo_count -= 1
    return render_template('timer.html')

@app.route("/collection")
def collection():
    if user == False:
        return redirect('/')
    return render_template('collection.html')

if __name__ == "__main__":
    app.run(debug = True)