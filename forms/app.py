
from flask import Flask, render_template, flash, redirect, url_for, request, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'


category_data = (
    (23, 'alpha'),
    (42, 'beta'),
)

subcategory_data = (
    (23, 1, 'aaa'),
    (23, 2, 'bbb'),
    (42, 7, 'foo'),
    (42, 8, 'bar'),
)

blank_option = (-1, '---')


class BasicForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name is required'), DataRequired('Name is empty')])
    category = SelectField('Category', coerce=int)
    subcategory = SelectField('Subcategory', coerce=int)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = BasicForm()

    form.category.choices = list(category_data)
    form.subcategory.choices = get_subcategories_for_category(form.category.choices[0][0])

    if form.validate_on_submit():
        print(f'category={form.category.data}({type(form.category.data)}) subcategory={form.subcategory.data}({type(form.subcategory.data)})')
        flash('Form ok!', 'info')
        return redirect(url_for('basic'))

    if form.errors:
        flash('Errors exist', 'error')

    return render_template('basic.html', form=form)


@app.route('/api/categories/')
def categories():
    return jsonify(category_data)


@app.route('/api/categories/<int:category>')
@app.route('/api/categories/<int:category>/subcategories')
def subcategories(category):
    options = get_subcategories_for_category(category)
    if not options:
        return abort(404)

    return jsonify(options)


def get_subcategories_for_category(category):
    return [i[1:] for i in subcategory_data if i[0] == category]
