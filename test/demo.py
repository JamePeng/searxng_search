from searxng_search.searxng_search import SearXNGSearch
from searxng_search.exceptions import RequestException, ParsingException, SearXNGSearchException

import logging

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- IMPORTANT ---
# Replace this with the actual base URL of your running SearXNG instance.
# If you set SEARXNG_HOSTNAME=localhost, use http://localhost or https://localhost (if internal TLS is enabled)
# If you set SEARXNG_HOSTNAME=your.lan.ip.address, use [http://your.lan.ip.address](http://your.lan.ip.address) or [https://your.lan.ip.address](https://your.lan.ip.address)
# If you set SEARXNG_HOSTNAME=your.domain.com, use [https://your.domain.com](https://your.domain.com)
SEARXNG_BASE_URL = "http://localhost:8080" # <-- ADJUST THIS BASED ON YOUR CADDY/SEARXNG_HOSTNAME SETTING!

def perform_text_search(keywords: str, language: str = "en-US"):
    """Demonstrates performing a text search with error handling."""
    logger.info(f"Performing text search for: '{keywords}' on {SEARXNG_BASE_URL}")

    # Use 'verify=False' if you're using Caddy's 'internal' TLS for localhost or LAN IP
    # and Python can't verify the self-signed certificate. For production with valid certs, keep 'True'.
    with SearXNGSearch(base_url=SEARXNG_BASE_URL, timeout=20, verify=False, retries=3, backoff_factor=0.5) as client:
        try:
            # Perform a general text search, requesting JSON format, limit to 8 results
            results = client.text(keywords, category="general", language=language, format="json", max_results=8)

            if results:
                logger.info(f"Successfully retrieved {len(results)} results for '{keywords}':")
                for i, result in enumerate(results):
                    logger.info(f"  Result {i+1}:")
                    logger.info(f"    Title: {result.get('title', 'N/A')}")
                    logger.info(f"    URL:   {result.get('href', 'N/A')}")
                    logger.info(f"    Body:  {result.get('body', 'N/A')}...")
            else:
                logger.info(f"No results found for '{keywords}'.")

        except RequestException as e:
            logger.error(f"Network or HTTP error during search: {e}")
        except ParsingException as e:
            logger.error(f"Error parsing SearXNG response: {e}")
        except ValueError as e:
            logger.error(f"Invalid input parameter: {e}")
        except SearXNGSearchException as e:
            logger.error(f"A general SearXNG search error occurred: {e}")
        except Exception as e:
            logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
    print("-" * 50) # Separator for clarity

if __name__ == "__main__":
    perform_text_search("Python programming best practices", language="en-US")
    perform_text_search("MCP是什么？", language="zh-CN")
    perform_text_search("nonexistent query xyz123") # Example for no results
    perform_text_search("") # Example for ValueError
