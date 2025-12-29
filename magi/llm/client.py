"""
LLM Client
==========

Abstraction layer for LLM providers with support for
modern OpenAI API (v1.0+) and future extensibility.
"""

from typing import Optional, Dict, Any, List, Protocol, runtime_checkable
from dataclasses import dataclass
import os


@runtime_checkable
class LLMClient(Protocol):
    """Protocol defining the LLM client interface."""
    
    @property
    def chat(self) -> Any:
        """Access chat completions API."""
        ...


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI client."""
    api_key: Optional[str] = None
    organization: Optional[str] = None
    base_url: Optional[str] = None
    timeout: float = 60.0
    max_retries: int = 3


def create_openai_client(
    api_key: Optional[str] = None,
    config: Optional[OpenAIConfig] = None
) -> Any:
    """
    Create an OpenAI client with modern API (v1.0+).
    
    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        config: Optional configuration object.
    
    Returns:
        OpenAI client instance.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not found. Install with: pip install openai>=1.0.0"
        )
    
    if config is None:
        config = OpenAIConfig()
    
    # Resolve API key
    resolved_key = api_key or config.api_key or os.getenv("OPENAI_API_KEY")
    
    if not resolved_key:
        raise ValueError(
            "OpenAI API key required. Provide via argument, config, or OPENAI_API_KEY env var."
        )
    
    client_kwargs = {
        "api_key": resolved_key,
        "timeout": config.timeout,
        "max_retries": config.max_retries,
    }
    
    if config.organization:
        client_kwargs["organization"] = config.organization
    
    if config.base_url:
        client_kwargs["base_url"] = config.base_url
    
    return OpenAI(**client_kwargs)


class MockLLMClient:
    """
    Mock LLM client for testing without API calls.
    """
    
    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self._responses = responses or {}
        self._call_count = 0
        self.chat = self._ChatCompletions(self)
    
    class _ChatCompletions:
        def __init__(self, parent: "MockLLMClient"):
            self._parent = parent
            self.completions = self
        
        def create(self, **kwargs) -> Any:
            self._parent._call_count += 1
            
            messages = kwargs.get("messages", [])
            last_message = messages[-1]["content"] if messages else ""
            
            # Check for matching response
            for key, response in self._parent._responses.items():
                if key.lower() in last_message.lower():
                    return self._make_response(response)
            
            # Default response based on expected format
            if kwargs.get("response_format", {}).get("type") == "json_object":
                return self._make_response('{"verdict": "info", "confidence": 0.7, "summary": "Mock response", "reasoning": "This is a test response."}')
            
            return self._make_response("This is a mock response from the MAGI system.")
        
        def _make_response(self, content: str) -> Any:
            class Choice:
                def __init__(self, content: str):
                    self.message = type("Message", (), {"content": content})()
            
            class Response:
                def __init__(self, content: str):
                    self.choices = [Choice(content)]
            
            return Response(content)
