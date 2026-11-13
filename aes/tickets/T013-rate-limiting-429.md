---
ticket: T013
title: Rate limiting e deteção de HTTP 429/403
sprint: sprint-03
priority: high
status: done
created: 2026-11-13
---

# T013 — Rate limiting e deteção de HTTP 429/403

## Contexto
Finding MAJOR T006-P2 da auditoria hostil: a biblioteca não deteta respostas HTTP 429 (Too Many Requests) nem 403 (Forbidden) do Google. Sem isto, o IP do utilizador pode ser bloqueado silenciosamente e `search()` itera para sempre sem resultados.

## Critérios de aceitação
- [ ] `get_page()` deteta resposta HTTP 429/403 e levanta exceção específica
- [ ] `search()` implementa backoff exponencial com retry limitado (máx. 3 tentativas)
- [ ] `pause` aumenta automaticamente após deteção de 429/403
- [ ] Testes unitários para 429/403 com mock (sem rede)
- [ ] `make lint` passa
- [ ] `make test` passa (35+ testes)
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py` (`get_page`, `search`), `tests/test_search.py`.
**Fora de scope:** alterações ao CLI.

## Dependências
T008 (timeout de rede já implementado).

## Rollback
Reverter alterações em `__init__.py` e `tests/test_search.py`.

## Riscos conhecidos
- Backoff exponencial aumenta tempo de execução em caso de bloqueio. Mitigação: limitar retries a 3.
- Deteção de 429 depende do código de status HTTP do Google, que pode mudar.

## Notas
Ticket derivado do finding T006-P2. Prioridade alta — protege o utilizador contra bloqueio de IP.
