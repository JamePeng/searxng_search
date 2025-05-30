# Changelog

## [0.1.0] - 2025-05-31

### Added

* **Initial Release of `searxng-search` library.**
* Core functionality to connect and interact with self-hosted SearXNG instances.
* Support for **text search** with customizable keywords, categories, language, and result limits.
* **Structured JSON output** for search results, making them easy to parse and integrate.
* Robust **error handling** for network issues, HTTP responses, and JSON parsing failures (`RequestException`, `ParsingException`).
* Clear documentation for installation, SearXNG setup (local and LAN with Docker/Caddy), and usage examples.
* Basic API reference for `SearXNGSearch` class and its `text` method.
* Continuous integration friendly structure with `pyproject.toml` and build tools.
* MIT License for open-source usage.

