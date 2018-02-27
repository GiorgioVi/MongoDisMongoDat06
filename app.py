from flask import Flask, render_template, redirect, url_for, request
import create

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("form.html")

@app.route('/results')
def results():
    return render_template("results.html")

if __name__ == "__main__":
    create.makeDatabase()
    app.debug = True
    app.run()