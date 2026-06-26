from typing import List, Dict, Any
from config.settings import TAVILY_API_KEY

class SearchService:
    """Wrapper class for searching the web."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or TAVILY_API_KEY

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Performs a web search query."""
        if not self.api_key:
            return [{"title": "Placeholder search result", "url": "https://example.com", "snippet": "Tavily API key not found. Run in mock mode."}]
            
        return [
            {"title": f"Tavily result for: {query}", "url": "https://example.com", "snippet": "Search result snippet description placeholder."}
        ]
