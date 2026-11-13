---
ticket: T001
title: Infraestrutura AES: kanban, CLAUDE.md, quality gates
sprint: sprint-01
priority: high
status: done
created: 2026-11-13
---

# T001 — Infraestrutura AES: kanban, CLAUDE.md, quality gates

## Contexto
O repositório `googlesearch` não tem qualquer estrutura AES. Sem `aes/kanban.md`, `CLAUDE.md` nem quality gates, não há rastreabilidade de decisões, nem critérios de "feito" verificáveis.

## Critérios de aceitação
- [ ] `aes/kanban.md` criado com estado global, sprints e tickets
- [ ] `aes/sprints/sprint-01.md` criado
- [ ] `aes/tickets/T001-aes-infraestrutura.md` criado (este ficheiro)
- [ ] `CLAUDE.md` criado com contrato operacional (comandos, nunca-fazer, ficheiros críticos)
- [ ] `docs/QUALITY_GATES.md` criado com critérios de validação por fase
- [ ] `docs/CHECKLIST.md` criado com checklist de pré-commit e pré-release
- [ ] Commit e push para `origin/master`

## Escopo
**Em scope:** ficheiros de configuração e documentação do protocolo AES.
**Fora de scope:** alterações ao código-fonte de `googlesearch/` ou testes.

## Dependências
Nenhuma.

## Rollback
Remover diretório `aes/` e ficheiros `CLAUDE.md`, `docs/QUALITY_GATES.md`, `docs/CHECKLIST.md`.

## Riscos conhecidos
- Nenhum (alterações apenas de documentação/configuração).

## Notas
Este ticket é a base para todos os próximos tickets AES no repositório.
