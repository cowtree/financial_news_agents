from typing import Dict, Any
from .base_agent import BaseAgent

class FormatterAgent(BaseAgent):
    """Agent responsible for formatting the final output into bullet points."""
    
    def __init__(self):
        super().__init__("Formatter")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the scored news items into a clean bullet-point format.
        
        Args:
            input_data: Dictionary containing scored news items
            
        Returns:
            Dictionary containing formatted output
        """
        scored_items = input_data.get('scored_items', [])
        formatted_items = []
        
        for item in scored_items:
            # Only include items with high relevance (score >= 7)
            if item['relevance_score'] >= 7:
                formatted_item = {
                    'bullet_point': f"• {item['original_title']}",
                    'summary': item['analysis'],
                    'source': item['source'],
                    'url': item['url'],
                    'relevance_score': item['relevance_score']
                }
                formatted_items.append(formatted_item)
        
        # Create the final formatted output
        formatted_output = []
        for item in formatted_items:
            formatted_output.append(item['bullet_point'])
            formatted_output.append(f"  {item['summary']}")
            formatted_output.append(f"  Source: {item['source']}")
            if item['url']:
                formatted_output.append(f"  URL: {item['url']}")
            formatted_output.append("")  # Add empty line for readability
        
        return {
            'formatted_output': formatted_output,
            'total_formatted': len(formatted_items)
        } 