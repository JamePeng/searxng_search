# Changelog

## [0.1.1] - 2025-06-08
### feat: Add retry mechanism for improved search reliability
This release introduces a retry mechanism to the SearXNGSearch class, significantly improving the success rate of fetching search results.

Key Changes:

* Retry Attempts: The __init__ method now accepts a retries parameter (defaulting to 3), allowing the client to automatically re-attempt failed HTTP requests.
* Exponential Backoff: A backoff_factor parameter (defaulting to 0.5) has been added to implement exponential backoff between retries. This helps prevent overwhelming the SearXNG instance and allows for recovery from transient network issues or service overloads.
* Enhanced _get_url: The internal _get_url helper now incorporates the retry logic, logging attempts and delays for better visibility into connection issues.

## [0.1.0] - 2025-05-31

### Initial

* **Initial Release of `searxng-search` library.**
* Core functionality to connect and interact with self-hosted SearXNG instances.
* Support for **text search** with customizable keywords, categories, language, and result limits.
* **Structured JSON output** for search results, making them easy to parse and integrate.
* Robust **error handling** for network issues, HTTP responses, and JSON parsing failures (`RequestException`, `ParsingException`).
* Clear documentation for installation, SearXNG setup (local and LAN with Docker/Caddy), and usage examples.
* Basic API reference for `SearXNGSearch` class and its `text` method.
* Continuous integration friendly structure with `pyproject.toml` and build tools.
* MIT License for open-source usage.

