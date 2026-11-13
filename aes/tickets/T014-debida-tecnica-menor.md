---
ticket: T014
title: Corrigir dívida técnica menor (findings MINOR da auditoria)
sprint: sprint-03
priority: medium
status: in-progress
created: 2026-11-13
---

# T014 — Corrigir dívida técnica menor

## Findings a corrigir (MINOR)
- T006-C2: Variável global `DEBUG` com `print()` — substituir por `logging` module
- T006-C3: Variáveis globais `_cookie_jar` e `_user_agents_list` não thread-safe
- T006-D3: `[bdist_wheel] universal = 1` obsoleto em `setup.cfg` (já corrigido em T0011)
- T006-CFG2: `extra_params` sem validação contra parâmetros conhecidos do Google

## Critérios de aceitação
- [ ] Substituir `DEBUG` global por `logging` module com nível configurável
- [ ] Adicionar `threading.Lock` para inicialização de `_cookie_jar` e `_user_agents_list`
- [ ] Adicionar validação básica de `extra_params` (parâmetros conhecidos do Google)
- [ ] `make lint` passa
- [ ] `make test` passa (38+ testes)
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py`.
**Fora de scope:** alterações à CLI ou arquitetura.

## Dependências
T013 (rate limiting já implementado).

## Rollback
Reverter alterações em `__init__.py`.

## Riscos conhecidos
- Mudar `DEBUG` para `logging` altera saída de debug (print -> log). Mitigação: manter comportamento equivalente.
- Thread lock adiciona pequena sobrecarga. Mitigação: lock apenas na inicialização lazy.

## Notas
Ticket derivado dos findings MINOR da auditoria hostil T006.
