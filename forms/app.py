
from flask import Flask, render_template, flash, redirect, url_for, request, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.widgets import Input
from wtforms.validators import InputRequired, DataRequired, ValidationError
from werkzeug.utils import escape
from markupsafe import Markup


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'


category_data = (
    (23, 'alpha'),
    (42, 'beta'),
)

valid_categories = [i[0] for i in category_data]

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

    def validate_subcategory(form, field):
        options = get_subcategories_for_category(form.category.data)
        if not options:
            raise ValidationError('Bad category')

        options = [i[0] for i in options]

        if field.data not in options:
            raise ValidationError('Subcategory not valid for category')


class PriceInput(Input):
    input_type = "number"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("step", "0.01")
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        return Markup("""
            <div style='display: inline-block'>
                <span>$</span>
                <input %s>
            </div>
        """ % self.html_params(name=field.name, **kwargs))


class PriceField(DecimalField):
    widget = PriceInput()


class PriceForm(FlaskForm):
    price = PriceField("Price")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = BasicForm()
    print(f'Name=[{escape(form.name.data)}]')

    form.category.choices = list(category_data)

    current_category = valid_categories[0]
    if form.category.data and form.category.data in valid_categories:
        current_category = form.category.data

    form.subcategory.choices = get_subcategories_for_category(current_category)

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


@app.route('/price', methods=['GET', 'POST'])
def price():
    form = PriceForm()

    if form.validate_on_submit():
        print(f'price={form.price.data}({type(form.price.data)})')
        flash('Form ok!', 'info')
        return redirect(url_for('price'))

    if form.errors:
        flash('Errors exist', 'error')

    return render_template('price.html', form=form)
