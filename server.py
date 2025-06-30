#!/usr/bin/env python3
"""
MCP Server for SwiftNotes Deep Research

This server exposes a 'deep_research' tool that allows LLMs to perform comprehensive research
by calling the SwiftNotes API's deep research endpoint.

The server properly implements the MCP protocol with:
- Tool listing capabilities (automatic with FastMCP)
- Tool calling capabilities (automatic with FastMCP)
- Proper schema definitions and error handling
- Integration with SwiftNotes API server

API Key Configuration:
Set the SWIFTNOTES_API_KEY environment variable or configure it in your MCP client.

Usage:
    SWIFTNOTES_API_KEY=your_key python mcp_server.py

The server will start and listen for MCP protocol messages on stdin/stdout.
"""

import asyncio
import os
import logging
from typing import Any, Dict

import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

# Configuration
SWIFTNOTES_API_BASE_URL = "https://api.swiftnotes.com"
DEFAULT_TIMEOUT = 300.0  # 5 minutes for research operations

# Initialize FastMCP server
mcp = FastMCP("SwiftNotes Deep Research Server")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # This should be called before accessing environment variables

def get_api_key() -> str:
    """
    Get API key from environment variables.
    
    Checks SWIFTNOTES_API_KEY first, then DEFAULT_API_KEY for backwards compatibility.
    
    Returns:
        API key string
        
    Raises:
        Exception: If no API key is found in environment variables
    """
    api_key = os.getenv("SWIFTNOTES_API_KEY")
    
    if not api_key:
        raise Exception(
            "No API key found in environment variables. "
            "Please set SWIFTNOTES_API_KEY environment variable."
        )
    
    return api_key

@mcp.tool()
async def deep_research(search_query: str) -> Dict[str, Any]:
    """
    Perform comprehensive research on a topic by analyzing YouTube content.
    
    This tool searches YouTube for videos related to the query, processes their transcripts,
    and generates a comprehensive research report with cited sources.
    
    Args:
        search_query: The research topic or question to investigate
        
    Returns:
        Dict containing:
        - title: The title of the generated research report
        - content: The main content of the report in Markdown format  
        - sources: Array of source objects with number, title, and url
        
    Raises:
        Exception: If the API call fails or returns an error
    """
    # Get API key from environment
    auth_api_key = get_api_key()
    
    # Validate search query
    if not search_query or not search_query.strip():
        raise Exception("Search query cannot be empty.")
    
    # Prepare the request
    headers = {
        'Authorization': f'Bearer {auth_api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'search': search_query.strip()
    }
    
    # Make the API call
    url = f"{SWIFTNOTES_API_BASE_URL}/deep_research"
    
    try:
        logger.info(f"Starting deep research for query: {search_query}")
        
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Research completed successfully for query: {search_query}")
                return {
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "sources": result.get("sources", [])
                }
            elif response.status_code == 401:
                raise Exception("Authentication failed. Invalid API key.")
            elif response.status_code == 403:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                raise Exception(f"Credit limit reached: {error_data.get('message', 'Please upgrade for higher volume needs.')}")
            elif response.status_code == 400:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                raise Exception(f"Bad request: {error_data.get('error', 'Invalid search query')}")
            else:
                # Try to get error message from response
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', f'HTTP {response.status_code}')
                except:
                    error_msg = f'HTTP {response.status_code}'
                logger.error(f"API call failed: {error_msg}")
                raise Exception(f"API call failed: {error_msg}")
                
    except httpx.TimeoutException:
        logger.error(f"Request timed out for query: {search_query}")
        raise Exception("Request timed out. The research is taking longer than expected.")
    except httpx.RequestError as e:
        logger.error(f"Request failed for query: {search_query}, error: {str(e)}")
        raise Exception(f"Request failed: {str(e)}")

if __name__ == "__main__":
    get_api_key()
    mcp.run(transport='stdio')
