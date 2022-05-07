from pydoc import doc
from flask import jsonify, request, make_response
from app import app
from app import db
from app import models

document_list = []


@app.route('/api/v1/index', methods=['POST'])
def add_document():
    document = models.Document(
        title=request.json.get('title', ""),
        body=request.json.get('body', ""),
    )
    db.session.add(document)
    db.session.commit()

    doc_tags = request.json.get('tags', "")
    for tag in doc_tags:
        tag_model = models.DocumentTag(tag_text=tag, doc=document)
        db.session.add(tag_model)
        db.session.commit()
    # print(request.json.get('tags', ""), 'requestststst')

    return make_response(f"{document} successfully created!")


# @app.route('/api/v1/search/<search_word>', methods=['GET'])
# def search_document(search_word):
#     matched_documents = []
#     related_documents = []
#     for item in document_list:
#         if((search_word in item['title']) or (search_word in item['body'])):
#             print('worrrdd')
#             matched_documents.append(item)

#         # for tag in item['tags']:
#         if((search_word in item['tags'])):
#             # If Item is already in the matched documents, do we need it in related?
#             related_documents.append(item)
#     documents = {
#         'matched_documents': matched_documents,
#         'related_documents': related_documents
#     }

#     return jsonify(documents), 200


@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    documents = models.Document.query.all()
    documents_schema = models.DocumentSchema(many=True)
    return jsonify(documents_schema.dump(documents))
