# agentic_rag_with_langgraph

A Retrieval-Augmented Generation (RAG) agentic pipeline using LangChain, LangGraph, and ChromaDB. This project demonstrates how to build a modular, extensible RAG system that fetches web content, indexes it for semantic search, and answers user questions using LLMs and agent workflows.

## Features
- **Web Document Loading:** Fetches and parses web pages for use as knowledge sources.
- **Chunking & Embedding:** Splits documents into token-aware chunks and generates dense embeddings using OpenAI models.
- **Vector Search:** Stores embeddings in ChromaDB for fast similarity search and retrieval.
- **Agentic Workflow:** Uses LangGraph to orchestrate agent nodes (retriever, rewriter, generator, etc.) for flexible multi-step reasoning.
- **Tool Integration:** Exposes retrieval as a tool for agent use, enabling complex chains and decision logic.
- **Extensible Nodes:** Includes document relevance checking, question rewriting, and answer generation nodes.

## Code Structure
```
├── src/
│   ├── main.py            # CLI entrypoint, runs the agentic RAG loop
│   ├── config.py          # Loads configuration/environment variables
│   ├── retriever/
│   │   └── tools.py       # Loads, splits, embeds, and indexes web docs; exposes retriever tool
│   └── agent/
│       ├── graph.py       # Defines the agent workflow graph (nodes, edges, conditions)
│       ├── nodes.py       # Implements agent nodes: analyze, rewrite, generate, etc.
│       └── state.py       # Agent state definition (TypedDict)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE
```

## How It Works
1. **Startup:**
   - Loads config and environment variables (OpenAI API key required).
   - Sets up the retriever tool by fetching, chunking, embedding, and indexing web pages.
   - Builds the agent workflow graph with nodes for retrieval, rewriting, relevance checking, and answer generation.
2. **User Interaction:**
   - Prompts the user for a question in the CLI.
   - Runs the question through the graph, which decides (based on document relevance) whether to answer, rewrite, or retrieve more info.
   - Streams or returns the final answer.

## Usage
### 1. Install Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the repo root:
```
OPENAI_API_KEY=sk-...
```

### 3. Run the Agent
```powershell
python src\main.py
```

### 4. Ask Questions
- Type your question at the prompt.
- Type `exit` or `quit` to terminate.

## Customization
- **Change Source URLs:** Edit `src/retriever/tools.py` to modify the list of web pages indexed.
- **Tune Chunk Size/Overlap:** Adjust `chunk_size` and `chunk_overlap` in the text splitter for different retrieval granularity.
- **Add/Modify Nodes:** Extend `src/agent/nodes.py` to add new agent behaviors or tools.
- **Switch LLM Model:** Change the `model_name` in ChatOpenAI instantiations to use different OpenAI models.

## Troubleshooting
### Streaming Error: Organization Not Verified
If you see:
```
Your organization must be verified to stream this model. Please go to: ...
```
**Solution:**
- Edit all `ChatOpenAI(..., streaming=True)` to `streaming=False` in the codebase (especially in `src/agent/nodes.py`).
- Restart the program. This disables streaming and avoids the org verification requirement.

### Other Issues
- Ensure your OpenAI API key is valid and has sufficient quota.
- If ChromaDB re-embeds on every run, consider persisting the vector store to disk.
- For debugging, use the included notebook (`notebooks/debugging.ipynb`).

## Code Highlights
- **main.py:** Orchestrates the RAG pipeline, handles user input, and prints results.
- **tools.py:** Shows how to build a retriever tool from web data, including chunking and embedding.
- **graph.py:** Demonstrates agentic workflows with conditional edges and multi-step reasoning.
- **nodes.py:** Implements modular agent nodes for relevance checking, rewriting, and answer generation.

## Extending This Project
- Add more document sources (PDFs, local files, APIs).
- Integrate additional tools (calculators, search APIs, etc.) for richer agent capabilities.
- Add evaluation scripts or tests for agent performance.
- Deploy as a web service or integrate with chat platforms.

## License
MIT

## Acknowledgments
This project was based on the original Scoras Academy Practical AI Projects repository.

https://github.com/Scoras-Academy/Projetos_Praticos_de_IA/blob/main/Projetos_praticos_de_IA/Ferramenta%20de%20Gera%C3%A7%C3%A3o%20Automatica%20de%20Relat%C3%B3rios.ipynb


## Authors
Vinicius Kos
---

**This project is a template for building agentic RAG systems with LangChain and LangGraph. Fork, extend, and adapt for your own knowledge retrieval and QA needs!**