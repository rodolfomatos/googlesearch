---
ticket: T007
title: Corrigir findings de segurança (SSL, cookie jar, user-agent)
sprint: sprint-02
priority: high
status: done
created: 2026-11-13
---

# T007 — Corrigir findings de segurança

## Findings a corrigir
- T006-S1 (MAJOR): `--insecure` desativa verificação SSL sem aviso ao utilizador
- T006-S2 (MAJOR): Cookie jar em `~/.google-cookie` sem chmod 600 (texto simples)
- T006-S3 (MINOR): User-agent padrão IE 8 desatualizado (2009)
- T006-S4 (MINOR): Playwright usa `--no-sandbox` sem documentação

## Critérios de aceitação
- [ ] `--insecure` emite aviso (`warnings.warn`) no stderr quando usado
- [ ] Cookie jar ficheiro recebe `chmod 600` após gravação
- [ ] User-agent padrão atualizado para browser moderno
- [ ] `--no-sandbox` documentado no CLAUDE.md como necessário em containers
- [ ] `make lint` passa
- [ ] `make test` passa (32 testes)
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `googlesearch/__init__.py`, `googlesearch/__main__.py`, `CLAUDE.md`.
**Fora de scope:** alterações à arquitetura, novos testes de integração com rede.

## Dependências
T006 (auditoria hostil concluída).

## Rollback
Reverter alterações em `__init__.py`, `__main__.py`, `CLAUDE.md`.

## Riscos conhecidos
- Adicionar `warnings.warn` pode quebrar código que capture stderr de forma rígida. Mitigação: usar `warnings.warn` padrão do Python.

## Notas
Ticket derivado do finding T006. Segurança é prioridade alta.
