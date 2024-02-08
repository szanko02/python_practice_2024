import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()
elasticsearch_url = os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch(elasticsearch_url)

index_name = "posts"
index_config = {
    "mappings": {
        "properties": {
            "iD": {"type": "keyword"},
            "text": {"type": "text"},
            "rubrics": {"type": "keyword"},
            "created_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
        }
    }
}

def create_index():
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index {index_name} deleted")
    else:
        print(f"Index {index_name} does not exist")

    es.indices.create(index=index_name, body=index_config)
    print(f"Index {index_name} created")

if __name__ == "__main__":
    create_index()