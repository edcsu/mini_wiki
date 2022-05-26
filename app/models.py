from datetime import datetime

from marshmallow_sqlalchemy import auto_field
from sqlalchemy import ForeignKey
from app import db
from sqlalchemy.dialects.sqlite import TEXT
from app import ma

from app.search import add_to_index, remove_from_index, query_index

document_tag = db.Table('documnet_tag',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
class Document(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(600))
    body = db.Column(db.TEXT())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=document_tag, backref='docs')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(200))

class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    tags = ma.Nested(TagSchema, many=True)
    class Meta:
        model = Document
        load_instance = True

db.create_all()

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)