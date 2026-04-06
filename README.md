# Vectorless RAG

A Retrieval-Augmented Generation system that eliminates the need for vector embeddings and vector databases entirely.

Instead of converting documents into embedding vectors and performing similarity search, this system uses **PageIndex** to extract a hierarchical tree structure from PDFs, then uses an **LLM to reason** over that tree to identify which nodes are relevant to a query — before retrieving their text to generate a grounded answer.

---

## Why Vectorless?

Traditional RAG pipelines require:
- An embedding model to encode chunks
- A vector database (FAISS, Pinecone, Chroma, etc.) to store and search them
- Chunking strategies that often break document structure

This approach replaces all of that with **document-structure-aware reasoning**:

| | Traditional RAG | Vectorless RAG |
|---|---|---|
| Retrieval method | Vector similarity search | LLM reasoning over document tree |
| Requires embedding model | Yes | No |
| Requires vector database | Yes | No |
| Preserves document structure | Rarely | Always |
| Retrieval is explainable | No | Yes (thinking trace) |

---

## Pipeline

```
PDF
 └─► PageIndex API ──► Document Tree (nodes with titles + summaries)
                              │
                              ▼
                    LLM reasons over tree
                    "Which nodes answer this query?"
                              │
                              ▼
                    Relevant node IDs
                              │
                              ▼
                    Extract node text (relevant context)
                              │
                              ▼
                    LLM generates grounded answer
```

---

## Project Structure

```
├── pageindex_tree.py          # Step 1: Index a PDF, cache doc_id
├── reasoning_based_retrieval.py  # Step 2: LLM picks relevant nodes from tree
├── answer_generation.py       # Step 3: Extract context, generate answer
├── setup_llm.py               # Async OpenAI wrapper
└── data/                      # Place your PDF files here
```

---

## Setup

```bash
git clone https://github.com/yourusername/vectorless-rag.git
cd vectorless-rag

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:
```
PAGEINDEX_API_KEY=your_pageindex_api_key
OPENAI_API_KEY=your_openai_api_key
```

Get your PageIndex API key at [pageindex.ai](https://pageindex.ai).

---

## Usage

**Step 1 — Index your document** (run once per PDF):
```bash
python pageindex_tree.py
```
This submits the PDF to PageIndex, waits for processing, and caches the `doc_id` locally in `doc_cache.json`. Subsequent runs skip re-submission automatically.

**Step 2 — Ask a question**:
```bash
python answer_generation.py
```

Output includes:
1. Retrieved node titles and page numbers
2. LLM's reasoning trace (which nodes it chose and why)
3. Retrieved context excerpt
4. Final generated answer

To change the document or query, edit the `doc_path` and `query` variables in `answer_generation.py`.

---

## Example Output

```
Retrieved Nodes:
Node ID: node_3   Page: 2   Title: Attention Mechanism Overview
Node ID: node_7   Page: 5   Title: Scaled Dot-Product Attention
Node ID: node_12  Page: 8   Title: Multi-Head Attention

Reasoning:
The query asks about the attention mechanism. Node 3 provides a high-level
overview, node 7 explains the core mathematical operation, and node 12
covers the multi-head variant which is central to the Transformer...

Retrieved Context:
## Attention Mechanism Overview
An attention function can be described as mapping a query and a set of
key-value pairs to an output...

Generated Answer:
The attention mechanism computes a weighted sum of values, where the weight
assigned to each value is determined by a compatibility function of the query
with the corresponding key...
```

---

## How It Works

**Tree-based retrieval** — PageIndex parses the PDF's structure (sections, subsections, figures) into a JSON tree. Each node has a title, summary, and full text. The LLM receives only titles and summaries (not full text) to reason about which nodes are relevant — keeping the context window small even for large documents.

**Transparent reasoning** — The LLM outputs a `thinking` trace explaining why it selected each node, making retrieval decisions fully auditable.

**Doc ID caching** — Once a document is indexed, its `doc_id` is stored locally. Every subsequent query reuses the existing index without re-uploading the PDF.
