# searxng_search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client library crafted by **JamePeng (jame_peng@sina.com)** for seamless interaction with your self-hosted [SearXNG](https://docs.searxng.org/) instance. This library empowers you to programmatically perform various searches (text, images, videos, news, etc.) against your local or LAN-deployed SearXNG server, giving you full control over your search data without relying on external APIs.

---

## Features

* **Connect to Local/LAN SearXNG:** Easily specify the base URL (IP address and port) of your self-hosted SearXNG instance, supporting both local and network-accessible deployments.
* **Text Search:** Perform general web searches and retrieve structured results.
* **Structured Output:** Receive search results in a clean, parseable JSON format.
* **Robust Error Handling:** Comprehensive error management for network issues, server responses, and parsing failures.
* **Customizable:** Extendable to support more SearXNG categories and search types.

---

## Installation

### Prerequisites

* **Python 3.8+**: Ensure you have a compatible Python version installed.
* **Docker & Docker Compose**: (Recommended for setting up SearXNG) Make sure Docker and Docker Compose are installed on your system.

### Install the `searxng_search` Library

You can install `searxng_search`  by building it from source.


#### From Source

Clone the repository (or create the project structure):

```bash
git clone https://github.com/jamepeng/searxng_search.git
cd searxng_search
```

Alternatively, manually create the following directory structure and files within your project root:

```
searxng_search_package/
├── searxng_search/
│   ├── __init__.py
│   ├── searxng_search.py
│   ├── exceptions.py
│   └── utils.py
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```


Install build tools:

```bash
pip install build wheel setuptools
```

Build the package:

```bash
python -m build
```

Install the generated wheel file:

```bash
pip install ./dist/searxng_search-0.1.0-py3-none-any.whl
```

### Setting up SearXNG with Docker (Recommended)

Before using `searxng_search`, you'll need a running SearXNG instance. This setup uses `searxng-docker`'s recommended `docker-compose.yaml` with Caddy as a reverse proxy, suitable for both local and external (LAN/public) access.

Clone the `searxng-docker` repository:

```bash
git clone https://github.com/searxng/searxng-docker.git
cd searxng-docker
```

Adjust `docker-compose.yaml` and `Caddyfile`:

The provided `docker-compose.yaml` is designed for use with Caddy and Redis. Here's the configuration for your `docker-compose.yaml`:

```yaml
version: "3.7"
services:
  caddy:
    container_name: caddy
    image: docker.io/library/caddy:2-alpine
    network_mode: host # Binds to host network, allowing direct port access (e.g., 80/443)
    restart: unless-stopped
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy-data:/data:rw
      - caddy-config:/config:rw
    environment:
      # Define your SearXNG hostname here.
      # For local access, set to "localhost" or "127.0.0.1".
      # For LAN/Internet access, set to your domain or public IP (e.g., "mysearxng.com").
      - SEARXNG_HOSTNAME=${SEARXNG_HOSTNAME:-localhost} # Default to localhost
      - SEARXNG_TLS=${LETSENCRYPT_EMAIL:-internal} # For internal HTTPS or Let's Encrypt email
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"

  redis:
    container_name: redis
    image: docker.io/valkey/valkey:8-alpine # Using Valkey as a Redis fork
    command: valkey-server --save 30 1 --loglevel warning
    restart: unless-stopped
    networks:
      - searxng
    volumes:
      - valkey-data2:/data # Changed volume name for clarity
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"

  searxng:
    container_name: searxng
    image: docker.io/searxng/searxng:latest
    restart: unless-stopped
    networks:
      - searxng
    # Expose SearXNG's port only to the local machine, as Caddy will handle external access
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      # Mount a volume for SearXNG's settings.yml.
      # You might want to copy a default settings.yml from the container first.
      - ./searxng:/etc/searxng:rw
    environment:
      # SearXNG's internal base URL, should point to where Caddy exposes it.
      - SEARXNG_BASE_URL=https://${SEARXNG_HOSTNAME:-localhost}/
      - UWSGI_WORKERS=${SEARXNG_UWSGI_WORKERS:-4}
      - UWSGI_THREADS=${SEARXNG_UWSGI_THREADS:-4}
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"

networks:
  searxng: # Custom network for inter-service communication

volumes:
  caddy-data: # Persists Caddy's certificates and data
  caddy-config: # Persists Caddy's configuration
  valkey-data2: # Persists Valkey (Redis) data
```

Create a `Caddyfile` in the same directory as `docker-compose.yaml`:

```caddyfile
{$SEARXNG_HOSTNAME} {
    log {
        output stdout
        level INFO
    }

    @searxng host {$SEARXNG_HOSTNAME}
    handle @searxng {
        reverse_proxy searxng:8080
    }

    # Enable HTTPS (optional, for external access with valid domain)
    # For internal/localhost, Caddy provides self-signed certificates by default.
    tls {$SEARXNG_TLS}
}
```

**Important Configuration Notes for Local and LAN Access:**

  * **`SEARXNG_HOSTNAME`**: This environment variable in `docker-compose.yaml` and `Caddyfile` dictates how SearXNG is accessed.
      * **For local access only**: Set `SEARXNG_HOSTNAME=localhost` in your `.env` file (or directly in `docker-compose.yaml`). You'll then access SearXNG via `http://localhost` or `https://localhost` (if Caddy's internal TLS is enabled).
      * **For LAN/public access**: Set `SEARXNG_HOSTNAME=your.lan.ip.address` (e.g., `192.168.1.100`) or `SEARXNG_HOSTNAME=your.domain.com`. You **must** also ensure your host's firewall and/or router forwards ports 80 (HTTP) and 443 (HTTPS) to the machine running Docker. This allows other devices on your network to reach the SearXNG server.
  * **`SEARXNG_TLS`**:
      * For **external domains**, provide a valid email (e.g., `LETSENCRYPT_EMAIL=your@email.com`) to enable Let's Encrypt for automatic HTTPS.
      * For **local/LAN IP access or testing**, `internal` will generate self-signed certificates, which your browser might warn about but allows for encrypted connections.
  * **`ports` for `searxng` service**: `127.0.0.1:8080:8080` means SearXNG is only directly accessible from the Docker host itself on port 8080. Caddy acts as the front-end proxy, handling external access and routing. You don't need to change this mapping for LAN access, as Caddy (running in `network_mode: host`) handles the external ports.

Start the SearXNG containers:

Navigate to the `searxng-docker` directory (where your `docker-compose.yaml` is) and run:

```bash
docker-compose up -d
```

This will pull the necessary images and start the Caddy, Redis, and SearXNG containers.

Verify SearXNG is running:

  * **Local Access:** Open your web browser and go to `http://localhost` or `https://localhost` (if `SEARXNG_TLS` is `internal`).
  * **LAN Access:** From another device on your local network, open your web browser and go to `http://your.lan.ip.address` or `https://your.lan.ip.address` (if `SEARXNG_TLS` is `internal`). If you configured a domain, use `https://your.domain.com`.

You should see the SearXNG search interface.

-----

## Usage Examples

Here's how you can use the `searxng_search` library in your Python code:

```python
import logging
from searxng_search import SearXNGSearch, RequestException, ParsingException, SearXNGSearchException

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- IMPORTANT ---
# Replace this with the actual base URL of your running SearXNG instance.
# If you set SEARXNG_HOSTNAME=localhost, use http://localhost or https://localhost (if internal TLS is enabled)
# If you set SEARXNG_HOSTNAME=your.lan.ip.address, use [http://your.lan.ip.address](http://your.lan.ip.address) or [https://your.lan.ip.address](https://your.lan.ip.address)
# If you set SEARXNG_HOSTNAME=your.domain.com, use [https://your.domain.com](https://your.domain.com)
SEARXNG_BASE_URL = "http://localhost" # <-- ADJUST THIS BASED ON YOUR CADDY/SEARXNG_HOSTNAME SETTING!

def perform_text_search(keywords: str):
    """Demonstrates performing a text search with error handling."""
    logger.info(f"Performing text search for: '{keywords}' on {SEARXNG_BASE_URL}")

    # Use 'verify=False' if you're using Caddy's 'internal' TLS for localhost or LAN IP
    # and Python can't verify the self-signed certificate. For production with valid certs, keep 'True'.
    with SearXNGSearch(base_url=SEARXNG_BASE_URL, timeout=60, verify=True) as client:
        try:
            # Perform a general text search, requesting JSON format, limit to 5 results
            results = client.text(keywords, category="general", format="json", max_results=5)

            if results:
                logger.info(f"Successfully retrieved {len(results)} results for '{keywords}':")
                for i, result in enumerate(results):
                    logger.info(f"  Result {i+1}:")
                    logger.info(f"    Title: {result.get('title', 'N/A')}")
                    logger.info(f"    URL:   {result.get('href', 'N/A')}")
                    logger.info(f"    Body:  {result.get('body', 'N/A')[:100]}...") # Truncate body for display
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
    perform_text_search("Python programming best practices")
    perform_text_search("latest AI advancements 2025")
    perform_text_search("nonexistent query xyz123") # Example for no results
    perform_text_search("") # Example for ValueError
```

-----

## API Reference (Planned)

### `SearXNGSearch(base_url: str, headers: dict | None = None, timeout: int | None = 30, verify: bool = True)`

Initializes the client.

  * `base_url` (`str`): The full URL to your SearXNG instance (e.g., `"http://192.168.1.100:8080/"` or `"https://your.domain.com/"`).
  * `headers` (`dict`, optional): Custom HTTP headers for requests.
  * `timeout` (`int`, optional): Request timeout in seconds. Defaults to 30.
  * `verify` (`bool`, optional): Whether to verify SSL certificates. Set to `False` for self-signed certificates (e.g., Caddy's internal TLS or custom certs) if you encounter SSL errors, but keep `True` for production with valid certificates. Defaults to `True`.

### `SearXNGSearch.text(keywords: str, category: str = "general", language: str = "en-US", pageno: int = 1, format: Literal["json", "html"] = "json", max_results: int | None = None) -> list[dict[str, str]]`

Performs a text search.

  * `keywords` (`str`): The search query.
  * `category` (`str`, optional): SearXNG category (e.g., `"general"`, `"science"`, `"it"`, `"images"`, `"videos"`, `"news"`). Defaults to `"general"`.
  * `language` (`str`, optional): Language parameter for SearXNG (e.g., `"en-US"`, `"zh-CN"`). Defaults to `"en-US"`.
  * `pageno` (`int`, optional): Page number of results to fetch. Defaults to 1.
  * `format` (`Literal["json", "html"]`, optional): Desired output format from SearXNG. `"json"` is highly recommended for structured data. Defaults to `"json"`.
  * `max_results` (`int`, optional): Maximum number of results to return from the client side. If `None`, all results from the requested page are returned.

-----

## Exceptions

  * `SearXNGSearchException`: Base exception for all library errors.
  * `RequestException`: Raised for HTTP communication issues (network errors, timeouts, 4xx/5xx status codes).
  * `ParsingException`: Raised when SearXNG's response cannot be decoded or parsed as expected (e.g., invalid JSON, unexpected HTML structure).
  * `ValueError`: Raised for invalid input parameters provided to library methods.

-----

## Contributing

Contributions are welcome\! If you find a bug, have a feature request, or want to improve the code, please feel free to:

  * **Open an Issue:** Describe the bug or feature you'd like to see.
  * **Submit a Pull Request:** Fork the repository, create a new branch, make your changes, and submit a pull request.

-----

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

## Author

JamePeng (jame\_peng@sina.com)
