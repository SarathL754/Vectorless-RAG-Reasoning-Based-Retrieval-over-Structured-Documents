import asyncio
import json
from dotenv import load_dotenv
import pageindex.utils as utils
from setup_llm import call_llm
from reasoning_based_retrieval import reasoning_based_retrieval, _get_tree

load_dotenv()


async def generate_answer(query, doc_path="data/Attention.pdf", call_llm_func=call_llm):
    # Step 1: Retrieve relevant nodes via LLM reasoning over the tree
    tree_search_result = await reasoning_based_retrieval(query, doc_path=doc_path, call_llm_func=call_llm_func)

    # Step 2: Show reasoning
    tree_search_result_json = json.loads(tree_search_result)
    print('\nReasoning:\n')
    utils.print_wrapped(tree_search_result_json['thinking'])

    # Step 3: Extract text from retrieved nodes
    tree = _get_tree(doc_path)
    node_map = utils.create_node_mapping(tree)
    node_list = tree_search_result_json["node_list"]
    relevant_content = "\n\n".join(node_map[node_id]["text"] for node_id in node_list)

    print('\nRetrieved Context:\n')
    utils.print_wrapped(relevant_content[:1000] + '...')

    # Step 3: Generate answer grounded in retrieved context
    answer_prompt = f"""Answer the question based on the context:

Question: {query}
Context: {relevant_content}

Provide a clear, concise answer based only on the context provided.
"""

    print('\nGenerated Answer:\n')
    answer = await call_llm_func(answer_prompt)
    utils.print_wrapped(answer)

    return answer


if __name__ == "__main__":
    query = "What is the attention mechanism in neural networks?"
    asyncio.run(generate_answer(query))
