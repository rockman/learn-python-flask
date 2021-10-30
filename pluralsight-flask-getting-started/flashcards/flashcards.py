
from flask.helpers import url_for
from models import db
from flask import Flask, render_template, abort, request, redirect

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


@app.route('/add_card')
def add_card():
    return render_template('add_card.html')


@app.post('/add_card')
def do_add_card():
    try:
        db.append(dict(
            question=request.form['question'],
            answer=request.form['answer']
        ))
    except:
        pass
    return redirect(url_for('card', index=len(db) - 1))


@app.route('/remove/<int:index>')
def remove(index):
    return render_template('remove_card.html', card=db[index], index=index)


@app.post('/remove/<int:index>')
def do_remove(index):
    del db[index]
    return redirect(url_for('welcome'))
