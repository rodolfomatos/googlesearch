---
ticket: T0010
title: Melhorar CI (format check, mypy, prevenir testes de rede)
sprint: sprint-02
priority: high
status: done
created: 2026-11-13
---

# T0010 — Melhorar CI/CD

## Findings a corrigir
- T006-I1 (MAJOR): Sem `ruff format --check` nem mypy no CI
- T006-I2 (MAJOR): Regressão de testes de rede não prevenida
- T006-I3 (MINOR): Python 3.13 não testado

## Critérios de aceitação
- [ ] `.github/workflows/ci.yml` adiciona `ruff format --check`
- [ ] `.github/workflows/ci.yml` adiciona `mypy` (ou `pyright`) para verificação de tipos
- [ ] Adicionar comentário/pré-commit que proíba testes de rede no `tests/`
- [ ] Adicionar Python 3.13 à matriz de CI
- [ ] `make lint` passa localmente
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `.github/workflows/ci.yml`, `.travis.yml`, `tests/` (comentário).
**Fora de scope:** alterações ao código-fonte.

## Dependências
T005 (type hints devem existir antes de mypy no CI).

## Rollback
Reverter alterações em `.github/workflows/ci.yml`.

## Riscos conhecidos
- mypy pode reportar erros em código existente sem type hints. Mitigação: usar `--ignore-missing-imports` ou configurar mypy adequadamente.
- Python 3.13 pode não ter pacotes disponíveis no CI. Mitigação: testar e remover se falhar.

## Notas
Ticket derivado do finding T006. Infraestrutura de CI.
