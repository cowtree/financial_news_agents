# Financial News Aggregator

An agentic AI system that aggregates and summarizes relevant financial news.

Runs entirely on an open-source model (e.g. Qwen) served locally by oMLX
through its OpenAI-compatible API. No paid API key needed.

## Features

- Fetches financial news from public RSS feeds (CNBC, MarketWatch, Yahoo Finance)
- Analyzes and summarizes content
- Scores news relevance
- Formats output into concise bullet points

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start a local oMLX server, then create a `.env` file:
```
OMLX_API_KEY=your-omlx-api-key
OMLX_MODEL=Qwen3.6-35B-A3B-MLX-8bit
OMLX_THINKING=false
```
`OMLX_BASE_URL` is optional and defaults to `http://localhost:8000/v1`.
Any OpenAI-compatible local server (oMLX, Ollama, vLLM, LM Studio) works.

## Usage

Run the main script:
```bash
python src/main.py
```

## Architecture

The system consists of several specialized agents:

1. **Orchestrator Agent**: Coordinates the workflow
2. **News Fetcher Agent**: Retrieves financial news
3. **Content Analyzer Agent**: Analyzes and summarizes content
4. **Relevance Scorer Agent**: Scores news relevance
5. **Formatter Agent**: Formats final output 