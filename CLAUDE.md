# CLAUDE.md — googlesearch

Contrato operacional para o projeto `googlesearch` (bindings não oficiais do Google search).

## Identidade
- Single-file Python library (`googlesearch/__init__.py`, ~343 LOC) que faz scraping do Google via `urllib` + `BeautifulSoup`.
- CLI em `googlesearch/__main__.py` e wrapper `scripts/google`.
- Nome no PyPI: `google`; nome de importação: `googlesearch`.
- Versão atual: 3.1.0.

## Comandos essenciais
| Ação | Comando |
|------|---------|
| Instalar CLI (sem pip) | `make install` |
| Instalar editável (pip) | `make install-pip` |
| Executar testes | `make test` (`python -m unittest tests.test_search -v`) |
| Lint | `make lint` (`ruff check googlesearch/ tests/`) |
| Formatar | `make format` (`ruff format googlesearch/ tests/`) |
| Limpar caches | `make clean` |
| Desinstalar | `make uninstall` |

## Nunca fazer
- Não adicionar compatibilidade Python 2 nem `BeautifulSoup` antigo (não-bs4) — ambos removidos intencionalmente.
- Não adicionar dependências HTTP externas (`requests`, `httpx`, etc.) — zero deps além de `beautifulsoup4`.
- Não refatorar o uso de `vars()` em `get_tbs()` nem a flag global `DEBUG` — pré-existentes, estáveis, documentados.
- Não mover `from playwright.sync_api import sync_playwright` para o topo do ficheiro — a importação deve permanecer diferida dentro da função para que a biblioteca funcione sem Playwright instalado.
- Não alterar o seletor HTML `soup.find(id="search")` sem atualizar também a documentação de áreas frágeis.

## Ficheiros críticos
| Ficheiro | Papel |
|----------|-------|
| `googlesearch/__init__.py` | Core: `search()`, `lucky()`, `get_tbs()`, `filter_result()`, `get_page()`, fallback Playwright |
| `googlesearch/__main__.py` | CLI (`argparse`) |
| `scripts/google` | Wrapper instalado por `make install` (embeds `%ROOT%`) |
| `tests/test_search.py` | 13 testes (1 integração ao Google ao vivo) |
| `pyproject.toml` | Metadados do pacote (fonte de verdade) |
| `setup.py` | Shim fino que chama `setup()` sem argumentos |
| `Makefile` | Targets: `install`, `install-pip`, `test`, `lint`, `format`, `clean`, `uninstall` |
| `aes/kanban.md` | Estado global do projeto (fonte de verdade AES) |

## Não-goals
- Suporte a Python 2.
- Suporte a `BeautifulSoup` 3 (não-bs4).
- Dependências HTTP além de `beautifulsoup4`.

## Evidência requerida antes de declarar um task como feito
- Testes passam (`make test` → exit 0).
- Lint passa (`make lint` → exit 0).
- Formato correto (`ruff format --check` sem diff).
- Docs atualizados se o comportamento mudou.
- Diffstory escrito na saída de build (o que mudou, porquê, o que ficou intocado, riscos restantes).

## Revisão de pares
Antes de pushar para `origin/master`, o task deve passar por revisão crítica (simplicidade, correção para todos os inputs identificados, ausência de dívida técnica não justificada).
