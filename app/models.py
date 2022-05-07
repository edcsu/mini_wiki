from datetime import datetime
from app import db
from sqlalchemy.dialects.sqlite import TEXT
from app import ma
class Document(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(600))
    body = db.Column(db.TEXT())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship('DocumentTag', backref='doc', lazy='dynamic')

    def __repr__(self):
        return '<Document {}>'.format(self.title)


class DocumentTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(200))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))

    def __repr__(self):
        return '<DocumentTag {}>'.format(self.tag_text)

class DocumentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Document
    id = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
    timestamp = ma.auto_field()
    tags = ma.auto_field()

class DocumentTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DocumentTag
        # include_fk = True

db.create_all()
