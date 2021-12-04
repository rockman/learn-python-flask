
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'


class BasicForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name is required'), DataRequired('Name is empty')])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = BasicForm()

    if form.validate_on_submit():
        flash('Form ok!', 'info')
        return redirect(url_for('basic'))

    if form.errors:
        flash('Errors exist', 'error')

    return render_template('basic.html', form=form)
