🚀 Vectorless RAG: Reasoning-Based Retrieval over Structured Documents

A lightweight implementation of a next-generation Retrieval-Augmented Generation (RAG) system that eliminates vector embeddings and vector databases, replacing similarity-based retrieval with reasoning over document structure.

This project demonstrates an emerging paradigm shift in RAG systems — moving from "retrieving similar text" to "reasoning about where the answer exists within a document."

💡 Motivation

Traditional RAG pipelines rely on:

Chunking documents into small pieces
Encoding them into embeddings
Retrieving based on vector similarity

However, this approach introduces fundamental limitations:

❌ Loss of document structure due to chunking
❌ Semantic similarity ≠ actual relevance
❌ Poor performance on long, structured documents (papers, contracts, reports)

Recent research and industry developments suggest a new direction:

Retrieval should be driven by reasoning over structure, not similarity.

Vectorless RAG (e.g., PageIndex) follows this idea by treating documents as hierarchical systems instead of flat text.

🧠 Core Idea

Instead of the traditional pipeline:

Document → Chunks → Embeddings → Vector DB → Similarity Search → Answer

This system follows:

Document → Hierarchical Tree → Reasoning-Based Navigation → Retrieval → Answer
A document is represented as a tree (like a Table of Contents)
Each node contains:
title
summary
reference to content
An LLM reasons over this structure to locate relevant sections

👉 This mimics how humans read documents:

Scan structure → identify section → read relevant part

This paradigm is known as reasoning-first retrieval.

⚙️ Key Features
🚫 No vector database
🚫 No embedding model
🚫 No arbitrary chunking
🌲 Hierarchical tree-based indexing
🧠 LLM-driven reasoning for retrieval
🔍 Explainable and traceable retrieval paths
📄 Optimized for long, structured documents

Compared to traditional RAG:

Feature	Traditional RAG	Vectorless RAG
Retrieval method	Vector similarity	Reasoning over structure
Embeddings required	Yes	No
Vector DB required	Yes	No
Structure preserved	No	Yes
Explainability	Low	High
🧪 System Pipeline
PDF
 └─► PageIndex API ──► Document Tree (hierarchical index)
                              │
                              ▼
                    LLM reasons over tree
                    "Which nodes answer this query?"
                              │
                              ▼
                    Relevant node IDs
                              │
                              ▼
                    Extract node text (context)
                              │
                              ▼
                    LLM generates grounded answer

This aligns with the two-step architecture of vectorless RAG:

Build a structured tree index
Perform reasoning-based retrieval
📁 Project Structure
├── pageindex_tree.py             # Step 1: Index PDF → build tree
├── reasoning_based_retrieval.py  # Step 2: Select relevant nodes
├── answer_generation.py          # Step 3: Generate answer from context
├── setup_llm.py                  # Async LLM wrapper
└── data/                         # Input PDF documents
⚙️ Setup
git clone https://github.com/yourusername/vectorless-rag.git
cd vectorless-rag

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

Create a .env file:

PAGEINDEX_API_KEY=your_pageindex_api_key
OPENAI_API_KEY=your_openai_api_key
🚀 Usage
Step 1 — Index Document
python pageindex_tree.py
Uploads PDF to PageIndex
Builds hierarchical tree
Stores doc_id locally
Step 2 — Ask Questions
python answer_generation.py

Output includes:

Retrieved node titles and page references
LLM reasoning trace (why nodes were selected)
Context extracted from document
Final generated answer
🧾 Example Output
Retrieved Nodes:
Node 3 → Attention Overview
Node 7 → Scaled Dot-Product Attention
Node 12 → Multi-Head Attention

Reasoning:
The query relates to attention mechanisms. Node 3 provides overview,
Node 7 explains computation, Node 12 extends to multi-head usage.

Generated Answer:
The attention mechanism computes a weighted sum of values...
🧠 How It Works
🌲 Tree-Based Indexing

The document is transformed into a hierarchical structure:

Chapters → Sections → Subsections

This preserves context and relationships, unlike chunking.

🧠 Reasoning-Based Retrieval

Instead of similarity scoring, the LLM:

analyzes node summaries
selects relevant branches
navigates the tree

👉 Retrieval becomes a decision-making process, not a lookup.

🔍 Explainability

Each answer includes:

reasoning trace
exact section references

This makes the system auditable, unlike vector similarity scores.

📊 Why This Matters

Vectorless RAG represents a fundamental shift:

Old Paradigm	New Paradigm
"Find similar text"	"Find where the answer lives"
Statistical retrieval	Reasoning-driven retrieval
Flat text chunks	Structured document navigation

This approach is particularly effective for:

financial reports
legal contracts
research papers
technical manuals

Where structure and reasoning matter more than similarity.

🚀 Future Work
Multi-document reasoning
Hybrid RAG (vector + reasoning)
Vision-based document understanding
Agentic tree traversal
Benchmarking against vector RAG systems
📚 References
https://pageindex.ai/blog/pageindex-intro
https://techcommunity.microsoft.com/blog/azuredevcommunityblog/vectorless-reasoning-based-rag-a-new-approach-to-retrieval-augmented-generation/4502238