from crypt import methods
from flask import jsonify, request
from app import app

document_list = []
# @app.route("/index", methods=['POST'])
@app.route('/api/v1/index', methods=['POST'])
def add_document():
    document = {
                'title':request.json.get('title', ""),
                'body': request.json.get('body', ""),
                'tags':request.json.get('tags', "")
                }
    document_list.append(document)
    return jsonify({'document':document}), 201

@app.route('/api/v1/search/<search_word>', methods=['GET'])
def search_document(search_word):
    matched_documents = []
    related_documents = []
    for item in document_list:
        if((search_word in item['title']) or (search_word in item['body'])):
            print('worrrdd')
            matched_documents.append(item)

        # for tag in item['tags']:
        if((search_word in item['tags'])):
            # If Item is already in the matched documents, do we need it in related?
            related_documents.append(item)
    documents = {
        'matched_documents': matched_documents,
        'related_documents': related_documents
    }

    return jsonify(documents), 200

@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    return jsonify(document_list)

