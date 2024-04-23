from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Create a Flask Instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.root_path, "users.db")
# Add secret key for crg
app.config['SECRET_KEY'] = 'my secret key'

# Initialize the database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)

    # Create a string
    def __repr__(self):
        return '<Users %r>' % self.name

 #Create a Form Class
class WelcomeForm(FlaskForm):
    name = StringField("What's your name? ", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.route('/')
def index():
    first_name = 'Itika'
    return render_template('index.html', fname=first_name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',uname=name)

# Create name page
@app.route('/welcome', methods=['GET','POST'])
def welcome():
    name = None
    form = WelcomeForm()

    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

        
        flash("Form Submitted Successfully!!!")

    return render_template("welcome.html", name=name, form=form)

# Create name page
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()

    # Validate form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added!!!")
    
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, name=name, our_users=our_users )

if __name__ == '__main__':
    app.run(debug=True)



