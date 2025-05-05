import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from .base_agent import BaseAgent
import logging

class NewsFetcherAgent(BaseAgent):
    """Agent responsible for fetching financial news from various sources."""
    
    def __init__(self):
        super().__init__("NewsFetcher")
        self.sources = [
            "https://www.reuters.com/markets/",
            "https://www.bloomberg.com/markets",
            "https://www.ft.com/markets"
        ]
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch financial news from configured sources.
        
        Args:
            input_data: Dictionary containing any parameters for fetching
            
        Returns:
            Dictionary containing fetched news items
        """
        news_items = []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        for source in self.sources:
            try:
                self.logger.info(f"Fetching news from {source}")
                response = requests.get(source, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                self.logger.info(f"Successfully fetched content from {source}")
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try different selectors for different news sites
                articles = []
                if 'reuters.com' in source:
                    articles = soup.select('article h3')[:5]
                elif 'bloomberg.com' in source:
                    articles = soup.select('.headline__text')[:5]
                elif 'ft.com' in source:
                    articles = soup.select('.js-teaser-heading-link')[:5]
                
                self.logger.info(f"Found {len(articles)} articles from {source}")
                
                for article in articles:
                    title = article.get_text().strip()
                    url = article.find_parent('a')['href'] if article.find_parent('a') else None
                    
                    if title:
                        news_items.append({
                            'title': title,
                            'source': source,
                            'url': url
                        })
                        self.logger.info(f"Added article: {title}")
            
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching from {source}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Unexpected error processing {source}: {str(e)}")
        
        self.logger.info(f"Total news items fetched: {len(news_items)}")
        return {
            'news_items': news_items,
            'total_items': len(news_items)
        } 