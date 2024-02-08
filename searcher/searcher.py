import csv
import os
from flask import Flask, jsonify, request, render_template
from elasticsearch import Elasticsearch
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
elasticsearch_url = os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch(elasticsearch_url)

from index_creation import create_index
index_name = "posts"

@app.route("/index_data", methods=["POST"])
def index_data():
    with open('./posts.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            es.index(index=index_name, document=row)
    return jsonify({"message": "Data indexed successfully"})

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get("query")
    try:
        results = search_documents(query) if query else []
        return jsonify(results)  
    except Exception as e:
        error_message = f"An error occurred during the search: {str(e)}"
        return jsonify({"error": error_message})

def search_documents(query):
    search_query = {
        "query": {
            "match": {
                "text": {
                    "query": query   
                }
            }
        },
        "sort": {
            "created_date": "desc"
        },
        "size": 20
    }
    results = es.search(index=index_name, body=search_query)
    hits = results["hits"]["hits"]
    return hits


@app.route("/delete/<doc_id>", methods=["DELETE"])
def delete_doc(doc_id):
    if request.method == "DELETE":
        try:
            es.delete(index=index_name, id=doc_id)
            return jsonify({"message": f"Document with ID {doc_id} deleted successfully"})
        except Exception as e:
            return jsonify({"message": f"Failed to delete document with ID {doc_id}: {str(e)}"})

if __name__ == "__main__":
    create_index()
    app.run()
