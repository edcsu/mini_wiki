from flask import jsonify, request
from app import app

document_list = []

@app.route("/index", methods=['POST'])
def add_document():
    document = {
                'title':request.json.get('title', ""),
                'body': request.json.get('body', ""),
                'tags':request.json.get('tags', "")
                }
    document_list.append(document)
    return jsonify({'document':document}), 201

