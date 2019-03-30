import pyrebase
from flask import Flask, request, render_template, redirect
from config import config #config.py is a dictionary containing
app = Flask(__name__)

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()

@app.route("/", methods = ['GET', 'POST'])
def splash():
    return "HOMEPAGE"

@app.route("/login", methods = ['GET', 'POST'])
def login():
    invalid = 'Login invalid, please check your credentials.'
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pass']
        try: 
            user = auth.sign_in_with_email_and_password(email, password)
            #print(auth.get_account_info(user['idToken']))
            return redirect('/home') #after login
        except:
            return render_template('login.html', fail = invalid)
    return render_template('login.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    invalid = 'Something went wrong with registration, please try again.'
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pass']
        data = {"name": request.form['user_name']}
        try: 
            user = auth.create_user_with_email_and_password(email, password)
            results = db.child("users").push(data, user['idToken'])
            #print(auth.get_account_info(user['idToken']))
            return redirect('/home')
        except:
            return render_template('register.html', fail = invalid)
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug = True)