---
ticket: T002
title: Testes para áreas frágeis (num != 10, CLI, teste ao vivo)
sprint: sprint-01
priority: high
status: done
created: 2026-11-13
---

# T002 — Testes para áreas frágeis

## Contexto
No `AGENTS.md` estão listadas três áreas frágeis com cobertura insuficiente:

1. **`num != 10`** — "historicamente buggy, ainda menos testado que o default `num=10`". Não existem testes para caminhos onde `num` difere de 10.
2. **CLI (`__main__.py`)** — zero testes de integração para a linha de comando (parsing de argumentos, ajuda, erro de query vazia).
3. **Teste ao vivo** — `test_returns_none_for_empty` faz um HTTP real ao Google; se o Google estiver fora ou mudar o HTML, o suite fica vermelho sem ser culpa do código.

## Critérios de aceitação
- [ ] Testes unitários para `search()` com `num=20`, `num=50`, `start > 0` (usando HTML fixture estático, sem rede)
- [ ] Testes de integração para o CLI (`__main__.py`): `--help`, query vazia, parsing de argumentos
- [ ] Substituir o teste ao vivo por fixture HTML estático (testes determinísticos, offline)
- [ ] `make test` passa com 100% de testes offline
- [ ] `make lint` passa
- [ ] Commit e push para `origin/master`

## Escopo
**Em scope:** `tests/test_search.py`, `tests/` (novos ficheiros de fixture), `googlesearch/__main__.py` (se precisar de ajustes para testabilidade).
**Fora de scope:** alterações à lógica de `search()` em `__init__.py`, alterações à documentação principal.

## Dependências
Nenhuma.

## Rollback
Reverter alterações em `tests/` e `__main__.py`.

## Riscos conhecidos
- Criar fixtures HTML que não correspondam exatamente ao HTML real do Google pode dar falso senso de segurança. Mitigação: usar fixtures baseados em estrutura real conhecida e documentar que o seletor `id="search"` pode mudar.

## Notas
Ticket derivado da hostil analysis da Opção 2 recomendada anteriormente.
