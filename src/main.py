import asyncio
import os
from dotenv import load_dotenv
from agents.orchestrator import OrchestratorAgent

async def main():
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Create and run the orchestrator
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute()
    
    # Print the results
    print("\n=== Financial News Summary ===\n")
    for line in result['final_output']:
        print(line)
    
    print("\n=== Statistics ===")
    stats = result['statistics']
    print(f"Total news fetched: {stats['total_news_fetched']}")
    print(f"Total analyzed: {stats['total_analyzed']}")
    print(f"Total scored: {stats['total_scored']}")
    print(f"Total formatted: {stats['total_formatted']}")

if __name__ == "__main__":
    asyncio.run(main()) 