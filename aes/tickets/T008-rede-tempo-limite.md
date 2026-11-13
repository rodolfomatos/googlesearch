---
ticket: T008
title: Adicionar timeout de rede e rate limiting / deteção 429
sprint: sprint-02
priority: high
status: done
created: 2026-11-13
---

# T008 — Adicionar timeout de rede e rate limiting / deteção 429

## Findings a corrigir
- T006-P1 (MAJOR): Sem timeout de rede em `get_page()` (`urlopen` sem timeout)
- T006-P2 (MAJOR): Sem rate limiting nem deteção de HTTP 429/403
- T006-P3 (MINOR): Request desnecessário à home do Google antes de cada busca

## Critérios de aceitação
- [ ] `urlopen()` recebe `timeout` padrão (ex: 10s) configurável via parâmetro
- [ ] `search()` deteta resposta HTTP 429/403 e aplica backoff exponencial com retry
- [ ] Avaliar remoção do request à home do Google (linha 259 de `__init__.py`)
- [ ] `make lint` passa
- [ ] `make test` passa (32 testes + novos)
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py` (`get_page`, `search`).
**Fora de scope:** alterações à CLI.

## Dependências
T007 (segurança deve estar feita primeiro para evitar regressões).

## Rollback
Reverter alterações em `__init__.py`.

## Riscos conhecidos
- Adicionar timeout pode quebrar requisições muito lentas intencionais. Mitigação: timeout alto (ex: 30s) e configurável.
- Backoff exponencial aumenta tempo de execução em caso de bloqueio. Mitigação: limitar número de retries.

## Notas
Ticket derivado do finding T006. Performance e robustez de rede.
