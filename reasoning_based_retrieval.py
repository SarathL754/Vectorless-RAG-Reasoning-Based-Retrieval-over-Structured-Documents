import asyncio
import json
import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
import pageindex.utils as utils
from setup_llm import call_llm
from pageindex_tree import _load_cache, create_tree_from_pageindex

load_dotenv()

pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))

def _get_tree(doc_path):
    cache = _load_cache()
    if doc_path not in cache:
        print(f"No cached doc_id for '{doc_path}'. Indexing document...")
        doc_id = create_tree_from_pageindex(doc_path)
    else:
        doc_id = cache[doc_path]
    return pi_client.get_tree(doc_id, node_summary=True)['result']

async def reasoning_based_retrieval(query, doc_path="data/Attention.pdf", call_llm_func=call_llm):
    
    tree = _get_tree(doc_path)
    tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])
    search_prompt = f"""
    You are given a question and a tree structure of a document.
    Each node contains a node id, node title, and a corresponding summary.
    Your task is to find all nodes that are likely to contain the answer to the question.

    Question: {query}

    Document tree structure:
    {json.dumps(tree_without_text, indent=2)}

    Please reply in the following JSON format:
    {{
        "thinking": "<Your thinking process on which nodes are relevant to the question>",
        "node_list": ["node_id_1", "node_id_2", ..., "node_id_n"]
    }}
    Directly return the final JSON structure. Do not output anything else.
    """

    tree_search_result = await call_llm_func(search_prompt)

    node_map = utils.create_node_mapping(tree)
    tree_search_result_json = json.loads(tree_search_result)

    print('\nRetrieved Nodes:')
    for node_id in tree_search_result_json["node_list"]:
        node = node_map[node_id]
        print(f"Node ID: {node['node_id']}\t Page: {node['page_index']}\t Title: {node['title']}")

    return tree_search_result

if __name__ == "__main__":
    query = "What is the attention mechanism in neural networks?"
    asyncio.run(reasoning_based_retrieval(query))