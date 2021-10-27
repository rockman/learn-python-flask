
from models import db
from flask import Flask, render_template, abort

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/card/<int:index>')
def card(index):
    try:
        return render_template('card.html', card=db[index])
    except IndexError:
        abort(404)