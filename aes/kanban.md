---
project: googlesearch
created: 2026-11-13
current_sprint: sprint-02
current_ticket: ""
---

# Kanban — googlesearch

## Estado global

| Campo | Valor |
|-------|-------|
| Projeto | googlesearch |
| Criado em | 2026-11-13 |
| Sprint atual | sprint-02 |
| Ticket atual | T0011 |

## Sprints

| Sprint | Período | Status | Tickets |
|--------|---------|--------|---------|
| sprint-01 | 2026-11-13 → 2026-11-20 | done | T001, T002, T003, T004, T005 |
| sprint-02 | 2026-11-13 → 2026-11-27 | active | T006, T007, T008, T009, T0010, T0011 |

## Tickets

| ID | Título | Sprint | Status | Prioridade |
|----|--------|--------|--------|------------|
| T001 | Infraestrutura AES: kanban, CLAUDE.md, quality gates | sprint-01 | done | high |
| T002 | Testes para áreas frágeis (num != 10, CLI, teste ao vivo) | sprint-01 | done | high |
| T003 | Testes de integração para o CLI (`__main__.py`) | sprint-01 | done | high |
| T004 | Substituir teste ao vivo por fixture HTML estático | sprint-01 | done | high |
| T005 | Type hints públicos (`search`, `filter_result`, `get_tbs`, etc.) | sprint-01 | done | medium |
| T006 | Auditoria hostil completa do projeto (11 domínios AES) | sprint-02 | done | high |
| T007 | Corrigir findings de segurança (SSL, cookie jar, user-agent) | sprint-02 | done | high |
| T008 | Adicionar timeout de rede e rate limiting / deteção 429 | sprint-02 | done | high |
| T009 | Melhorar cobertura de testes (get_page, Playwright, erros de rede) | sprint-02 | done | high |
| T0010 | Melhorar CI (format check, mypy, prevenir testes de rede) | sprint-02 | done | high |
| T0011 | Corrigir inconsistências de API (stop=0, pausa adaptativa, docs) | sprint-02 | done | medium |
| T012 | Atualizar documentação após mudanças do sprint-02 | sprint-02 | done | high |
| T013 | Rate limiting e deteção de HTTP 429/403 | sprint-03 | done | high |
| T014 | Corrigir dívida técnica menor (findings MINOR da auditoria) | sprint-03 | done | medium |
| T015 | Auditoria hostil final pós-sprint-03 | sprint-03 | done | high |

## Backlog

*Sprint-02 concluído. Sprint-03 concluído.*
