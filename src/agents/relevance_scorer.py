import openai
from typing import Dict, Any
from .base_agent import BaseAgent
import logging

class RelevanceScorerAgent(BaseAgent):
    """Agent responsible for scoring the relevance of news items."""
    
    def __init__(self, api_key: str):
        super().__init__("RelevanceScorer")
        openai.api_key = api_key
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
                
                Provide a score and brief justification.
                """
                
                # Call OpenAI API for scoring
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial news relevance scorer."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                score_analysis = response.choices[0].message['content']
                
                # Extract numerical score (assuming it's in the first line)
                score = 5  # default score
                try:
                    score = int(score_analysis.split('\n')[0].strip())
                except:
                    pass
                
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