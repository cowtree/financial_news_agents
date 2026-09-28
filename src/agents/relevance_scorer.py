from typing import Dict, Any
from .base_agent import BaseAgent
from .llm import LocalLLM
import logging
import re

class RelevanceScorerAgent(BaseAgent):
    """Agent responsible for scoring the relevance of news items."""
    
    def __init__(self, llm: LocalLLM):
        super().__init__("RelevanceScorer")
        self.llm = llm
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score the relevance of analyzed news items.
        
        Args:
            input_data: Dictionary containing analyzed news items
            
        Returns:
            Dictionary containing scored news items
        """
        analyzed_items = input_data.get('analyzed_items', [])
        scored_items = []
        
        for item in analyzed_items:
            try:
                # Create a prompt for scoring
                prompt = f"""
                Score the relevance of this financial news (1-10):
                
                Title: {item['original_title']}
                Analysis: {item['analysis']}
                
                Consider:
                1. Market impact
                2. Timeliness
                3. Global significance
                4. Industry relevance
                
                Start your answer with the score on its own line (e.g. "Score: 8"),
                then give a brief justification.
                """
                
                # Call the local model for scoring
                score_analysis = self.llm.chat("You are a financial news relevance scorer.", prompt)
                
                # Extract the numerical score from the first line
                score = 5  # default score
                match = re.search(r'\b(10|[1-9])\b', score_analysis.strip().split('\n')[0])
                if match:
                    score = int(match.group(1))
                
                scored_items.append({
                    **item,
                    'relevance_score': score,
                    'score_justification': score_analysis
                })
                self.logger.info(f"Successfully scored article: {item['original_title']} with score {score}")
                
            except Exception as e:
                self.logger.error(f"Error scoring news item: {str(e)}")
        
        # Sort items by relevance score
        scored_items.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'scored_items': scored_items,
            'total_scored': len(scored_items)
        } 