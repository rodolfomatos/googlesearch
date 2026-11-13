---
ticket: T012
title: Atualizar documentação após mudanças do sprint-02
sprint: sprint-02
priority: high
status: done
created: 2026-11-13
---

# T012 — Atualizar documentação após mudanças do sprint-02

## Contexto
Após as mudanças do sprint-02 (segurança, timeout, CI, consistência de API), vários documentos estão desatualizados:

- `AGENTS.md`: não menciona parâmetro `timeout`, não documenta avisos de segurança
- `README.md`: tabela de parâmetros da API não inclui `timeout`
- `CLAUDE.md`: não registra mudanças de segurança nem novo parâmetro

## Critérios de aceitação
- [ ] `AGENTS.md`: adicionar `timeout` aos parâmetros de `get_page()` e `search()`
- [ ] `AGENTS.md`: documentar avisos de segurança (SSL desativado, cookie jar `chmod 600`)
- [ ] `README.md`: adicionar `timeout` à tabela de parâmetros da API
- [ ] `CLAUDE.md`: documentar mudanças de segurança e novo parâmetro `timeout`
- [ ] `make lint` passa
- [ ] `make test` passa (35 testes)
- [ ] `python ./setup.py --name` funciona
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `AGENTS.md`, `README.md`, `CLAUDE.md`.
**Fora de scope:** alterações ao código-fonte.

## Dependências
T007-T011 (mudanças de código já concluídas).

## Rollback
Reverter alterações nos 3 documentos.

## Riscos conhecidos
- Nenhum (alterações apenas de documentação).

## Notas
Ticket criado para rastrear a atualização de documentação pendente do sprint-02.
