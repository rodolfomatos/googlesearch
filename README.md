# google-search

Unofficial Python bindings to the Google search engine. Scrapes Google results via
`urllib` + `BeautifulSoup`, with an optional **Playwright** backend for modern
JavaScript-based bot protection.

**Not affiliated with Google in any way.**

---

## Install

### Quick install (no pip)

```bash
make install
google --help
```

Installs the CLI to `~/.local/bin/google`. The script embeds the repo path so
it finds the Python module without `pip install`.

### Pip install

```bash
pip install google       # from PyPI (original: pip install google)
# or from checkout:
pip install -e .         # editable install, registers google-search entry point
```

### Playwright backend (recommended)

Google now serves a JavaScript challenge to automated scrapers. The `urllib`
backend alone will likely return zero results. Install Playwright for a working
experience:

```bash
pip install playwright --break-system-packages   # Ubuntu/Debian
playwright install chromium                      # download headless browser
```

Or via the optional dependency group:

```bash
pip install google[playwright]
```

---

## Usage

### Python

```python
from googlesearch import search

for url in search('"Breaking Code" WordPress blog', stop=20):
    print(url)
```

### CLI

```bash
# Basic search
google --stop=10 "python programming"

# Randomize user agent on each request
google --stop=5 --rua "opencode agents"

# Date range
google --stop=10 --tbs "qdr:m" "machine learning"

# Force Playwright backend (bypasses urllib entirely)
google --stop=5 --backend=playwright "opencode agents"

# Auto mode (default): try urllib, fall back to Playwright if blocked
google --stop=5 --backend=auto "opencode agents"
```

### Quick result (first match)

```python
from googlesearch import lucky

url = lucky("python exceptions")
# → "https://docs.python.org/3/tutorial/errors.html"
# Returns None if no results found.
```

### Date-range search

```python
import datetime
from googlesearch import search, get_tbs

tbs = get_tbs(
    datetime.date(2024, 1, 1),
    datetime.date(2024, 12, 31),
)
for url in search("AI", tbs=tbs, stop=10):
    print(url)
```

---

## API Reference

### `search()`

```python
def search(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: Optional[int] = None,
    pause: float = 2.0,
    country: str = "",
    extra_params: Optional[dict] = None,
    user_agent: Optional[str] = None,
    verify_ssl: bool = True,
    include_google_links: bool = False,
    backend: str = "auto",
) -> Generator[str, None, None]:
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | required | Search string. Must NOT be URL-encoded. |
| `tld` | `'com'` | Top-level domain (e.g. `'co.uk'`, `'de'`). |
| `lang` | `'en'` | Result language code. |
| `tbs` | `'0'` | Time limits (`'qdr:h'` = hour, `'qdr:d'` = day, `'qdr:m'` = month). |
| `safe` | `'off'` | Safe search (`'on'`, `'off'`, `'active'`). |
| `num` | `10` | Results per page. Historically buggy for values ≠10 (now fixed). |
| `start` | `0` | First result index. |
| `stop` | `None` | Last result to yield. `None` = unlimited (loop until empty page). |
| `pause` | `2.0` | Seconds between HTTP requests. Too low → Google blocks your IP. |
| `country` | `''` | Region restrict. Similar to TLD but not identical. |
| `extra_params` | `{}` | Extra URL params. Overlaps with built-ins raise `ValueError`. |
| `user_agent` | `None` | Custom User-Agent string. |
| `verify_ssl` | `True` | Verify SSL certificates. |
| `include_google_links` | `False` | Whether to include links pointing to `google.*`. |
| `backend` | `'auto'` | `'urllib'`, `'playwright'`, or `'auto'` (try urllib, fall back). |

### `lucky()`

```python
def lucky(*args, **kwargs) -> Optional[str]:
```

Same arguments as `search()`. Returns the first URL or `None` if empty.

### `get_tbs()`

```python
def get_tbs(from_date: datetime.date, to_date: datetime.date) -> str:
```

Formats dates into Google's `tbs` parameter.

### `get_random_user_agent()`

```python
def get_random_user_agent() -> str:
```

Returns a random user agent from the built-in list (`user_agents.txt.gz`).

---

## Backend modes

The library ships two HTTP backends to cope with Google's bot protection:

| Backend | How it works |
|---------|-------------|
| `urllib` | Pure Python HTTP via standard library. Zero extra dependencies. **Likely blocked by Google's JavaScript challenge.** |
| `playwright` | Launches a headless Chromium browser that executes JavaScript. Handles the bot challenge transparently. Requires `playwright` + Chromium. |
| `auto` | Tries `urllib` first. If the response doesn't contain the expected `id=search` container (i.e. Google returned a challenge page), retries the same request with Playwright. |

**Recommendation:** Use `auto` (default). Without Playwright installed, `auto`
behaves identically to `urllib`.

---

## CLI reference

```
usage: google [-h] [--tld TLD] [--lang LANGUAGE] [--tbs TBS] [--safe SAFE]
              [--country COUNTRY] [--num N] [--start N] [--stop N]
              [--pause SECONDS] [--rua] [--insecure] [--include]
              [--backend {auto,urllib,playwright}]
              query [query ...]

positional arguments:
  query                 Search query

options:
  --tld TLD             Top level domain to use [default: com]
  --lang LANGUAGE       Produce results in the given language [default: en]
  --tbs TBS             Produce results from period [default: 0]
  --safe SAFE           Kids safe search [default: off]
  --country COUNTRY     Region to restrict search on [default: none]
  --num N               Number of results per page [default: 10]
  --start N             First result to retrieve [default: 0]
  --stop N              Last result to retrieve [default: unlimited]
  --pause SECONDS       Pause between HTTP requests [default: 2.0]
  --rua                 Randomize the User-Agent [default: no]
  --insecure            Disable SSL certificate verification [default: no]
  --include             Include links pointing to Google [default: no]
  --backend             {auto,urllib,playwright} [default: auto]
```

---

## Development

```bash
make install             # CLI → ~/.local/bin/google
make install-pip         # pip install -e .
make test                # unit tests
make lint                # ruff check
make format              # ruff format
make clean               # remove caches and build artifacts
make uninstall           # remove installed CLI and pip package
```

---

## Troubleshooting

### "No results" with urllib backend (default)

Google returns a JavaScript challenge page. Either:

1. **Install Playwright** (recommended):
   ```bash
   pip install playwright --break-system-packages
   playwright install chromium
   ```
   The `auto` backend will detect the block and switch automatically.

2. **Force Playwright**:
   ```bash
   google --backend=playwright "your query"
   ```

### CLI returns nothing but Python API works

Make sure to quote multi-word queries:
```bash
# Correct
google --stop=5 "opencode agents"

# Wrong (query is parsed as separate positional args)
google --stop=5 opencode agents
```

### Playwright complains about missing system deps

Chromium may require libraries. On Ubuntu/Debian:

```bash
playwright install-deps chromium
```

---

## Internals

- **`googlesearch/__init__.py`** (343 lines) — core logic
- **`googlesearch/__main__.py`** — CLI entry point
- **`scripts/google`** — standalone wrapper (used by `make install`)
- **`tests/test_search.py`** — 13 unit tests (1 integration test hits Google live)

Key architecture decisions:
- Zero HTTP dependencies beyond the stdlib (`urllib`)
- Playwright is **optional** — import is deferred until first use
- URL templates use `%`-formatting with explicit `template_params` dicts
- Cookie jar at `~/.google-cookie`, lazy-loaded
- User agents loaded from gzipped file at module init

---

## License

BSD 3-Clause. See `LICENSE`.
