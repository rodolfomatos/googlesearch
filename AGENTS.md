# googlesearch — Agent Guide

## Identity

Single-file Python library (`googlesearch/__init__.py`, 343 lines) that scrapes
Google search results via `urllib` + `BeautifulSoup`. CLI in
`googlesearch/__main__.py`. Versioned at `googlesearch.__version__`.

## Package gotcha

- PyPI name is `google`, import name is `googlesearch`.
  `pip install google` → `from googlesearch import search`.
- `setup.py` is a thin shim; real metadata lives in `pyproject.toml`.

## Dependencies

Only `beautifulsoup4` is required. Optional `playwright` backend handles Google's
JavaScript challenge — install with `pip install google[playwright]`.

## Commands

```bash
make install             # install CLI to ~/.local/bin/google (no pip needed)
make install-pip         # pip install -e . (editable, registers google-search entry point)
make test                # run unit tests
make lint                # ruff check
make format              # ruff format
```

CI (`.github/workflows/ci.yml`) runs `ruff check` then `pytest` across Python 3.7–3.12.

## Architecture notes

- **One entrypoint**: `search()` generator in `__init__.py:225`.
  `lucky()` wraps it with `next()`.
- **Backend auto-fallback**: `backend='auto'` tries `urllib` first. If the
  response lacks the `id=search` div (challenge page), it retries with
  Playwright.
- **No mocking in tests**: `test_returns_none_for_empty` makes a real HTTP
  request to Google (~2-3s). The other 12 tests are pure unit tests.
- **Cookie jar**: Stored at `~/.google-cookie`, lazy-loaded on first
  `search()` call.
- **User agents**: Loaded from `user_agents.txt.gz` (gzipped), also lazy.
- **Debug**: Set `googlesearch.DEBUG = True` to print raw HTML responses.

## Playwright backend internals

- `_check_playwright()` uses `importlib.util.find_spec("playwright")` — no
  import side effects.
- `_fetch_with_playwright()` applies stealth config to avoid Google's
  headless-browser detection:
  - `--disable-blink-features=AutomationControlled`
  - Overrides `navigator.webdriver`, `navigator.plugins`,
    `navigator.languages` via `add_init_script`
  - Visits google.com first (sets cookies), then navigates to the search URL
- Playwright import (`from playwright.sync_api import sync_playwright`) is
  deferred to inside `_fetch_with_playwright()` so that `search()`
  construction doesn't require it.

## Fragile areas

- **HTML selectors**: `soup.find(id='search')` is Google's current results
  container. Google changes HTML structure without notice. If results break,
  this selector is the first suspect.
- **URL templates**: `_url_search`, `_url_next_page`, etc. use
  `%`-formatting with named placeholders. Adding/changing URL params requires
  updating both template strings and the `template_params` dict in `search()`.
- **`num != 10` path**: Historically buggy (`%(safe)scr` typo — now fixed).
  Still less tested than the default `num=10` codepath.
- **Google bot detection**: Google's challenge page changes frequently.
  The `_fetch_with_playwright` stealth config may need updates.
- **CLI quoting**: Multi-word queries must be quoted (`"foo bar"`), not
  passed as separate positional args.

## What NOT to do

- Do not add Python 2 compatibility or old `BeautifulSoup` (non-bs4)
  support — both were intentionally removed.
- Do not add external HTTP dependencies (`requests`, `httpx`, etc.) — the
  library has zero deps beyond `beautifulsoup4`.
- Do not refactor the `get_tbs()` `vars()` usage or the global `DEBUG`
  flag — pre-existing, stable, documented.
- Do not move the `from playwright.sync_api import sync_playwright` import
  to the top of the file — it must remain deferred inside the function so
  the library works without playwright installed.
