from typing import Dict, Any
from .base_agent import BaseAgent
from .news_fetcher import NewsFetcherAgent
from .content_analyzer import ContentAnalyzerAgent
from .relevance_scorer import RelevanceScorerAgent
from .formatter import FormatterAgent
from .llm import LocalLLM

class OrchestratorAgent(BaseAgent):
    """Agent responsible for orchestrating the workflow between all other agents."""
    
    def __init__(self):
        super().__init__("Orchestrator")
        self.news_fetcher = NewsFetcherAgent()
        llm = LocalLLM()
        self.content_analyzer = ContentAnalyzerAgent(llm)
        self.relevance_scorer = RelevanceScorerAgent(llm)
        self.formatter = FormatterAgent()
    
    async def execute(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrate the workflow between all agents.
        
        Args:
            input_data: Optional dictionary containing any initial parameters
            
        Returns:
            Dictionary containing the final formatted output
        """
        # Step 1: Fetch news
        print("Fetching news...")
        news_data = await self.news_fetcher.execute({})
        
        # Step 2: Analyze content
        print("Analyzing content...")
        analyzed_data = await self.content_analyzer.execute(news_data)
        
        # Step 3: Score relevance
        print("Scoring relevance...")
        scored_data = await self.relevance_scorer.execute(analyzed_data)
        
        # Step 4: Format output
        print("Formatting output...")
        formatted_data = await self.formatter.execute(scored_data)
        
        return {
            'final_output': formatted_data['formatted_output'],
            'statistics': {
                'total_news_fetched': news_data['total_items'],
                'total_analyzed': analyzed_data['total_analyzed'],
                'total_scored': scored_data['total_scored'],
                'total_formatted': formatted_data['total_formatted']
            }
        } 