"""
Claude AI Client

Handles all interactions with Anthropic's Claude API for health recommendations.
Provides a clean interface for generating personalized health advice.
"""

import json
import asyncio
from typing import Dict, Optional, Any
import httpx
from datetime import datetime

# Import from our config
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import settings


class ClaudeAPIError(Exception):
    """Custom exception for Claude API errors"""
    pass


class ClaudeClient:
    """
    Client for interacting with Anthropic's Claude API.
    
    Provides methods for generating health recommendations based on 
    diabetes risk assessment data.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.
        
        Args:
            api_key (str, optional): Claude API key. Uses config if not provided.
        """
        self.api_key = api_key or settings.CLAUDE_API_KEY
        if not self.api_key:
            raise ClaudeAPIError("Claude API key is required")
        
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.CLAUDE_MAX_TOKENS
        self.timeout = settings.CLAUDE_TIMEOUT
        
        # HTTP client for API calls
        self.client = httpx.AsyncClient(
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            timeout=self.timeout
        )
    
    async def generate_health_recommendations(
        self, 
        prompt: str, 
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate health recommendations using Claude API.
        
        Args:
            prompt (str): The formatted prompt for Claude
            user_data (Dict): User data for context and logging
            
        Returns:
            Dict: Response containing recommendations and metadata
        """
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Make the API call
            response = await self.client.post(
                self.base_url,
                json=payload
            )
            
            # Handle response
            if response.status_code != 200:
                error_detail = f"API call failed with status {response.status_code}: {response.text}"
                raise ClaudeAPIError(error_detail)
            
            result = response.json()
            
            # Extract the recommendation text
            if "content" in result and len(result["content"]) > 0:
                recommendation_text = result["content"][0]["text"]
            else:
                raise ClaudeAPIError("No content in Claude response")
            
            # Return structured response
            return {
                "recommendation": recommendation_text,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat(),
                "user_context": {
                    "age": user_data.get("age"),
                    "activity_level": user_data.get("activity_level"),
                    "risk_level": user_data.get("diabetes_risk_level")
                },
                "api_usage": {
                    "input_tokens": result.get("usage", {}).get("input_tokens"),
                    "output_tokens": result.get("usage", {}).get("output_tokens")
                }
            }
            
        except httpx.RequestError as e:
            raise ClaudeAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise ClaudeAPIError(f"Failed to parse response: {str(e)}")
        except Exception as e:
            raise ClaudeAPIError(f"Unexpected error: {str(e)}")
    
    async def test_connection(self) -> bool:
        """
        Test the connection to Claude API with a simple request.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            test_prompt = "Please respond with 'Connection successful' to confirm the API is working."
            
            payload = {
                "model": self.model,
                "max_tokens": 50,
                "messages": [
                    {
                        "role": "user",
                        "content": test_prompt
                    }
                ]
            }
            
            response = await self.client.post(self.base_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if "content" in result and len(result["content"]) > 0:
                    return True
            
            return False
            
        except Exception:
            return False
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


# Convenience function for testing
async def test_claude_client():
    """Test Claude client functionality"""
    try:
        async with ClaudeClient() as client:
            print("🧪 Testing Claude API connection...")
            
            # Test connection
            is_connected = await client.test_connection()
            if is_connected:
                print("✅ Claude API connection successful!")
                
                # Test health recommendation
                test_data = {
                    "age": 45,
                    "activity_level": "moderate",
                    "diabetes_risk_level": "low-risk"
                }
                
                test_prompt = """
                Generate a brief health recommendation for a 45-year-old with moderate activity level and low diabetes risk.
                Keep it under 100 words and focus on maintaining their good health.
                """
                
                result = await client.generate_health_recommendations(test_prompt, test_data)
                print("✅ Health recommendation generation successful!")
                print(f"Response length: {len(result['recommendation'])} characters")
                
            else:
                print("❌ Claude API connection failed!")
                
    except ClaudeAPIError as e:
        print(f"❌ Claude API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    # Run test if executed directly
    print("Claude AI Client Test")
    print("=" * 30)
    asyncio.run(test_claude_client()) 