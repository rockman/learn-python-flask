
from re import A
from simple_forum.db import db
from simple_forum.models import Post, User, Tag

from flask import Flask, render_template, session, request, flash, url_for, redirect
from flask_migrate import Migrate

import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object('simple_forum.config')
    db.init_app(app)

    Migrate(app, db, render_as_batch=True)

    return app


app = create_app()


@app.template_filter('posts_length_string')
def posts_length_string(posts):
    n = len(posts)
    if n == 0:
        return 'are no posts'
    elif n == 1:
        return 'is 1 post'
    else:
        return f'are {n} posts'


@app.template_filter('format_date')
def format_date(dt):
    return datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M')


@app.route('/')
def posts():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    posts = Post.query.all()
    return render_template(
        'posts.html', 
        posts=posts,
        user=user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('posts'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('posts'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id = session.get('user_id')
    wanted_post_id = request.args.get('post_id')
    post = Post.query.filter_by(id=wanted_post_id, author_id=user_id).first()

    if request.method == 'POST':
        if 'save' == request.form.get('action'):
            title = request.form.get('title')
            body = request.form.get('body')

            if title and body:
                post.title = title
                post.body = body
                db.session.add(post)
                db.session.commit()

        elif 'delete' == request.form.get('action'):
            db.session.delete(post)
            db.session.commit()

        return redirect(url_for('posts'))

    if post:
        return render_template('edit.html', post=post)

    return redirect(url_for('posts'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('posts'))

    if request.method == 'POST':

        if 'cancel' == request.form.get('action'):
            return redirect(url_for('posts'))

        try:
            post = Post(
                author_id=user_id,
                title=request.form.get('title'),
                body=request.form.get('body')
            )
        except ValueError as e:
            flash(str(e))
            return render_template('create.html')

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('create.html')