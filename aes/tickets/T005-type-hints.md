---
ticket: T005
title: Type hints públicos (search, filter_result, get_tbs, etc.)
sprint: sprint-01
priority: medium
status: done
created: 2026-11-13
---

# T005 — Type hints públicos

## Contexto
A biblioteca `googlesearch` não tem type hints nas funções públicas (`search`, `lucky`, `get_tbs`, `get_random_user_agent`, `filter_result`). Isso dificulta a utilização por IDEs, ferramentas de análise estática (mypy, pyright), e desenvolvedores que consomem a biblioteca.

O projeto já suporta Python >=3.7 (conforme `pyproject.toml`), então type hints com `typing` (não `X | Y` syntax do 3.10+) são necessários para compatibilidade.

## Critérios de aceitação
- [ ] `search()` recebe type hints em todos os parâmetros e retorno (Generator[str, None, None])
- [ ] `lucky()` recebe type hints em parâmetros e retorno (Optional[str])
- [ ] `get_tbs()` recebe type hints em parâmetros (datetime.date, datetime.date) e retorno (str)
- [ ] `get_random_user_agent()` recebe type hints em retorno (str)
- [ ] `filter_result()` recebe type hints em parâmetros e retorno (Optional[str])
- [ ] `get_page()` recebe type hints em parâmetros e retorno (str)
- [ ] `__main__.py` `main()` recebe type hints (retorno None)
- [ ] `make lint` passa (ruff não flagga type hints como erro)
- [ ] `make test` passa (32 testes OK)
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py` (funções públicas), `googlesearch/__main__.py` (main).
**Fora de scope:** alterar comportamento das funções, adicionar mypy como dependência.

## Dependências
Nenhuma.

## Rollback
Remover type hints dos ficheiros alterados.

## Riscos conhecidos
- Type hints incorretos podem enganar ferramentas de análise estática. Mitigação: usar tipos precisos do módulo `typing`.
- Adicionar `from __future__ import annotations` pode ser necessário para compatibilidade com Python 3.7 se usarmos tipos complexos. Mitigação: evitar tipos que requerem 3.9+.

## Notas
Ticket do backlog do sprint-01. Último ticket do sprint atual.
