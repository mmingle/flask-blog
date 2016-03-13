from flask import Flask
from flask import render_template, request, redirect, url_for
from .forms import LoginForm
import flask.ext.login as flask_login
from app import app


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'admin': {'pw': 'admin'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user




@app.route('/')
@app.route('/index')
def index():
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    user = {'nickname':'Mark Mingle'}
    return render_template('index.html',
                           title='home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id