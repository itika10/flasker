from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

@app.route('/')
def index():
    first_name = 'Itika'
    return render_template('index.html', fname=first_name)

@app.route('/user/<name>')
def hello(name):
    return render_template('user.html',uname=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

