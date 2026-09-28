import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from .base_agent import BaseAgent
import logging

class NewsFetcherAgent(BaseAgent):
    """Agent responsible for fetching financial news from various sources."""
    
    def __init__(self):
        super().__init__("NewsFetcher")
        self.sources = [
            # RSS feeds are meant for programs to read; the sites' HTML pages block scrapers
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
            "https://feeds.content.dowjones.io/public/rss/mw_topstories",
            "https://finance.yahoo.com/news/rssindex"
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
            'Accept': 'application/rss+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        for source in self.sources:
            try:
                self.logger.info(f"Fetching news from {source}")
                response = requests.get(source, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                self.logger.info(f"Successfully fetched content from {source}")
                root = ET.fromstring(response.content)
                
                # Every RSS feed lists its articles as <item> elements
                articles = root.findall('./channel/item')[:5]
                
                self.logger.info(f"Found {len(articles)} articles from {source}")
                
                for article in articles:
                    title = (article.findtext('title') or '').strip()
                    url = (article.findtext('link') or '').strip() or None
                    
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