
from simple_forum.db import db


tags_to_posts = db.Table('tags_to_posts',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', secondary=tags_to_posts, backref=db.backref('tags', lazy=True))