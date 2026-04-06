import os
import json
from dotenv import load_dotenv
from pageindex import PageIndexClient
import pageindex.utils as utils

load_dotenv()
pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))

CACHE_FILE = "doc_cache.json"

def _load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def create_tree_from_pageindex(doc_path):
    """Creates a tree structure from the PageIndex API response for a given document path.
    Reuses a cached doc_id if the document was already submitted."""
    cache = _load_cache()

    if doc_path in cache:
        doc_id = cache[doc_path]
        print(f"Using cached document ID: {doc_id}")
    else:
        doc_id = pi_client.submit_document(doc_path)["doc_id"]
        print(f"Document submitted with ID: {doc_id}")
        while True:
            status = pi_client.get_document(doc_id)["status"]
            if status == "completed":
                break
            print("Waiting for document to be processed...")
        cache[doc_path] = doc_id
        _save_cache(cache)
        print("Document processed.")

    print("Fetching content...")
    tree = pi_client.get_tree(doc_id, node_summary=True)['result']
    print('Simplified Tree Structure of the Document:')
    utils.print_tree(tree)

    return doc_id

if __name__ == "__main__":
    doc_path = "data/Attention.pdf"
    create_tree_from_pageindex(doc_path)