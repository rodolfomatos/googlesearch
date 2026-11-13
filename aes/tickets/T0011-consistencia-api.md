---
ticket: T0011
title: Corrigir inconsistências de API (stop=0, pausa adaptativa, docs)
sprint: sprint-02
priority: medium
status: done
created: 2026-11-13
---

# T0011 — Corrigir inconsistências de API

## Findings a corrigir
- T006-A2 (MINOR): `--stop=0` na CLI significa ilimitado, mas na API `stop=0` é zero resultados
- T006-A3 (MINOR): `pause` não adaptativo (não reage a 429)
- T006-C1 (MAJOR): Uso de `vars()` em `get_tbs()` (ofuscado)
- T006-C2 (MINOR): Variável global `DEBUG` com `print()`
- T006-C3 (MINOR): Globais não thread-safe (`_cookie_jar`, `_user_agents_list`)
- T006-D2 (MINOR): Sem upper bound em `beautifulsoup4`
- T006-D3 (MINOR): `universal = 1` obsoleto em `setup.cfg`
- T006-CFG2 (MINOR): `extra_params` sem validação

## Critérios de aceitação
- [ ] `--stop=0` na CLI é consistente com a API (documentado ou corrigido)
- [ ] `vars()` substituído por f-string em `get_tbs()` (ou documentado como estável)
- [ ] `DEBUG` substituído por `logging` module (ou documentado)
- [ ] `setup.cfg` corrigido (`universal = 1` removido)
- [ ] `pyproject.toml` com upper bound em `beautifulsoup4`
- [ ] `make lint` passa
- [ ] `make test` passa
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py`, `googlesearch/__main__.py`, `pyproject.toml`, `setup.cfg`.
**Fora de scope:** alterações à arquitetura.

## Dependências
T007 (segurança primeiro).

## Rollback
Reverter alterações nos ficheiros listados.

## Riscos conhecidos
- Alterar `--stop=0` pode quebrar scripts existentes. Mitigação: documentar claramente.
- Substituir `vars()` pode introduzir regressão se houver variáveis locais inesperadas. Mitigação: testar `get_tbs()` exaustivamente.

## Notas
Ticket derivado do finding T006. Dívida técnica e consistência.
