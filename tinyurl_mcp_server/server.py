import os
import logging
import requests
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """Get TinyURL API key from environment variables"""
    api_key = os.getenv("TINYURL_API_KEY")
    if not api_key:
        raise ValueError("TINYURL_API_KEY environment variable must be set")
    return api_key

# Initialize FastMCP
mcp = FastMCP("tinyurl")

@mcp.tool()
def create_short_url(url: str) -> Dict[str, Any]:
    """
    Convert a long URL to a short link
    
    Parameters:
    - url: URL to be shortened
    
    Returns:
    - Dictionary containing short link information
    """
    try:
        api_key = get_api_key()
        endpoint = f"https://api.tinyurl.com/create?api_token={api_key}"
        
        # Prepare request parameters
        payload = {"url": url}
        
        # Set request headers
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        
        # Send API request
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        # Return API response
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"error": f"Unable to create short link: {str(e)}"}
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unknown error: {str(e)}")
        return {"error": f"Error occurred while creating short link: {str(e)}"}

def main():
    """Start MCP server"""
    logger.info("Starting TinyURL MCP service...")
    mcp.run()

if __name__ == "__main__":
    main()