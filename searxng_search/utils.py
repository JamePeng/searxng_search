from __future__ import annotations
from .exceptions import ParsingException
import json
import logging

logger = logging.getLogger("searxng_search.utils")

def _normalize(text: str) -> str:
    """Normalize text by stripping whitespace and replacing multiple spaces."""
    if not isinstance(text, str): # Make sure the text is a string
        return ""
    return ' '.join(text.split()).strip()

def _normalize_url(url: str) -> str:
    """Normalize URL by stripping leading/trailing whitespace."""
    if not isinstance(url, str): # Make sure the url is a string
        return ""
    return url.strip()

def json_loads(content: bytes) -> dict:
    """Safely loads JSON content from bytes."""
    try:
        decoded_content = content.decode('utf-8')
        return json.loads(decoded_content)
    except UnicodeDecodeError as e:
        error_message = f"Failed to decode content to utf-8. Content preview: {content[:100]}... Error: {e}"
        logger.error(error_message)
        raise ParsingException(error_message) from e
    except json.JSONDecodeError as e:
        error_message = f"Failed to decode JSON. Error: {e}. Content preview: {decoded_content[:200]}..."
        logger.error(error_message)
        raise ParsingException(error_message) from e
    except Exception as e:
        error_message = f"An unexpected error occurred during JSON loading: {type(e).__name__}: {e}"
        logger.critical(error_message, exc_info=True)
        raise ParsingException(error_message) from e