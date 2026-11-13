---
project: googlesearch
created: 2026-11-13
current_sprint: sprint-01
current_ticket: ""
---

# Kanban — googlesearch

## Estado global

| Campo | Valor |
|-------|-------|
| Projeto | googlesearch |
| Criado em | 2026-11-13 |
| Sprint atual | sprint-01 |
| Ticket atual | — |

## Sprints

| Sprint | Período | Status | Tickets |
|--------|---------|--------|---------|
| sprint-01 | 2026-11-13 → 2026-11-20 | active | T001, T002, T003 |

## Tickets

| ID | Título | Sprint | Status | Prioridade |
|----|--------|--------|--------|------------|
| T001 | Infraestrutura AES: kanban, CLAUDE.md, quality gates | sprint-01 | done | high |
| T002 | Testes para áreas frágeis (num != 10, CLI, teste ao vivo) | sprint-01 | done | high |
| T003 | Testes de integração para o CLI (`__main__.py`) | sprint-01 | done | high |

## Backlog

- T004: Substituir teste ao vivo por fixture HTML estático — coberto por T002 (TestSearchOfflineLucky)
- T005: Type hints públicos (`search`, `filter_result`, `get_tbs`, etc.)
