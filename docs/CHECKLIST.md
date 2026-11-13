# Checklist de Qualidade — googlesearch

Itens configurados como **BLOCKER** (bloqueia o merge) ou **WARNING** (não bloqueia, mas deve ser avaliado).

## Pre-commit (rápido)

| # | Item | Tipo | Verificação |
|---|------|------|-------------|
| 1 | Testes passam | BLOCKER | `make test` exit 0 |
| 2 | Lint passa | BLOCKER | `make lint` exit 0 |
| 3 | Formato correto | BLOCKER | `ruff format --check googlesearch/ tests/` sem diff |
| 4 | Sem debug no source | BLOCKER | `grep -rn "console.log\|pdb\|breakpoint\|print(" googlesearch/` vazio |
| 5 | Sem TODO no source | WARNING | `grep -rn "TODO\|FIXME\|XXX" googlesearch/` avaliado |
| 6 | Docs atualizadas | BLOCKER (se comportamento mudou) | `README.md`, `AGENTS.md` refletem a alteração |
| 7 | Diffstory escrito | WARNING | Descrição do que mudou, porquê, o que ficou intocado, riscos |

## Pre-release (completo)

| # | Item | Tipo | Verificação |
|---|------|------|-------------|
| R1 | Versão incrementada | BLOCKER | `googlesearch.__version__` atualizada |
| R2 | `pyproject.toml` válido | BLOCKER | `python ./setup.py --name` exit 0 |
| R3 | Build editável funciona | BLOCKER | `pip install -e .` em venv isolado |
| R4 | CLI instalável | BLOCKER | `make install` cria `~/.local/bin/google` funcional |
| R5 | Importação pública funciona | BLOCKER | `from googlesearch import search, lucky, get_tbs, get_random_user_agent, filter_result` |
| R6 | Teste ao vivo do Google (se aplicável) | WARNING | `test_returns_none_for_empty` passa (depende de rede) |
| R7 | Changelog atualizado | WARNING | `docs/CHANGELOG.md` reflete a release |

## Regras gerais

- Um item **BLOCKER** que falhar impede o commit/merge até ser resolvido.
- Um item **WARNING** que falhar não bloqueia, mas deve ser justificado no PR/commit.
- Itens marcados "se comportamento mudou" só se aplicam quando o task altera comportamento visível ao utilizador.
- Não marque itens como "feito" sem executar a verificação correspondente.
