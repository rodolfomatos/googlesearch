---
ticket: T009
title: Melhorar cobertura de testes (get_page, Playwright, erros de rede)
sprint: sprint-02
priority: high
status: done
created: 2026-11-13
---

# T009 — Melhorar cobertura de testes

## Findings a corrigir
- T006-T1 (MAJOR): Sem testes para `get_page()`, `_fetch_with_playwright()`, fallback de backend, erros de rede
- T006-T2 (MAJOR): Fixtures HTML estáticos não refletem Google real
- T006-T3 (MINOR): Sem testes de CLI para argumentos inválidos

## Critérios de aceitação
- [ ] Testes para `get_page()` com mock (sucesso, erro 403, timeout, resposta vazia)
- [ ] Teste para deteção de challenge page e fallback Playwright (mocked)
- [ ] Teste de integração opcional ao Google (marcado, só roda com flag explícita)
- [ ] Testes de CLI para argumentos inválidos (`--num 0`, `--num -1`, `--pause -1`)
- [ ] `make lint` passa
- [ ] `make test` passa
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `tests/test_search.py`, `tests/fixtures/`.
**Fora de scope:** alterações ao código-fonte de `__init__.py`.

## Dependências
T008 (timeout e rate limiting precisam ser testados).

## Rollback
Reverter alterações em `tests/`.

## Riscos conhecidos
- Teste de integração ao Google pode falhar por motivos externos (rede, bloqueio). Mitigação: marcar como opcional/skip por default.

## Notas
Ticket derivado do finding T006. Qualidade de teste.
