from __future__ import annotations

class SearXNGSearchException(Exception):
    """Base exception for searxng_search errors."""
    pass

class RequestException(SearXNGSearchException):
    """Raised for HTTP request errors when communicating with SearXNG."""
    pass

class ParsingException(SearXNGSearchException):
    """Raised when parsing SearXNG's response fails."""
    pass