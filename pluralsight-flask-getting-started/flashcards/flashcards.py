
from models import db
from flask import Flask, render_template, abort

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html', cards=db)


@app.route('/card/<int:index>')
def card(index):
    try:
        return render_template(
            'card.html',
            index=index,
            is_first=index == 0,
            is_last=index == len(db) - 1,
            card=db[index])
    except IndexError:
        abort(404)

@app.route('/api/hint/<int:index>')
def hint(index):
    try:
        return db[index]['question']
    except IndexError:
        abort(404)