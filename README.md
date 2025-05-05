# Financial News Aggregator

An agentic AI system that aggregates and summarizes relevant financial news.

## Features

- Fetches financial news from multiple sources
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

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

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