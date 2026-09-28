from typing import Dict, Any
from .base_agent import BaseAgent
from .llm import LocalLLM
import logging

class ContentAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing and summarizing news content."""
    
    def __init__(self, llm: LocalLLM):
        super().__init__("ContentAnalyzer")
        self.llm = llm
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and summarize news content using a local open-source model.
        
        Args:
            input_data: Dictionary containing news items to analyze
            
        Returns:
            Dictionary containing analyzed and summarized news
        """
        news_items = input_data.get('news_items', [])
        analyzed_items = []
        
        for item in news_items:
            try:
                # Create a prompt for the analysis
                prompt = f"""
                Analyze this financial news headline and provide a brief summary:
                Headline: {item['title']}
                
                Provide:
                1. A 2-3 sentence summary
                2. Key financial implications
                3. Potential market impact
                """
                
                # Call the local model for analysis
                analysis = self.llm.chat("You are a financial news analyst.", prompt)
                
                analyzed_items.append({
                    'original_title': item['title'],
                    'source': item['source'],
                    'url': item['url'],
                    'analysis': analysis
                })
                self.logger.info(f"Successfully analyzed article: {item['title']}")
                
            except Exception as e:
                self.logger.error(f"Error analyzing news item: {str(e)}")
        
        return {
            'analyzed_items': analyzed_items,
            'total_analyzed': len(analyzed_items)
        } 