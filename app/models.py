from app import db
from sqlalchemy.dialects.sqlite import TEXT

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(600))
    body = db.Column(db.TEXT())

    def __repr__(self):
        return '<Document {}>'.format(self.title)

# class DocumentTags(db.Model):
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
