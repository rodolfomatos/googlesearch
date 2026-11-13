---
ticket: T003
title: Testes de integração para o CLI (__main__.py)
sprint: sprint-01
priority: high
status: done
created: 2026-11-13
---

# T003 — Testes de integração para o CLI (__main__.py)

## Contexto
O CLI em `googlesearch/__main__.py` é o ponto de entrada para utilizadores via linha de comando. No T002 foram adicionados 3 testes iniciais para o CLI (--help, impressão de resultados, query unida com espaços), mas a cobertura é superficial. Precisamos de testes de integração mais completos que validem todos os argumentos do argparse, valores default, e comportamento edge-case.

## Critérios de aceitação
- [ ] Teste para cada argumento do argparse (--tld, --lang, --tbs, --safe, --country, --num, --start, --stop, --pause, --rua, --insecure, --include, --backend)
- [ ] Teste de valores default (--stop=0 → None, --num=10, --pause=2.0, etc.)
- [ ] Teste de query vazia ou inválida
- [ ] Teste de parâmetros passados corretamente para search() (verificação via mock dos kwargs)
- [ ] Teste de --stop=0 resulta em search com stop=None
- [ ] Testes offline (mock de googlesearch.__main__.search), zero dependência de rede
- [ ] make test passa com todos os testes CLI
- [ ] make lint passa
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `tests/test_search.py` (novos testes CLI), possivelmente ajustes mínimos em `googlesearch/__main__.py` se necessário para testabilidade.
**Fora de scope:** alterações à lógica de `search()` em `__init__.py`.

## Dependências
T002 (já concluído — estabeleceu a base de mock para o CLI).

## Rollback
Reverter alterações em `tests/test_search.py` relacionadas ao CLI.

## Riscos conhecidos
- Testar argparse via `main()` requer manipulação de `sys.argv`, que pode ter efeitos colaterais entre testes. Mitigação: salvar e restaurar `sys.argv` em cada teste.
- O `main()` itera sobre `search()` e imprime diretamente para stdout, o que dificulta testes de saída. Mitigação: mockar `search()` e verificar argumentos, não stdout.

## Notas
Ticket derivado do backlog do sprint-01. Parcialmente coberto por T002; este ticket complementa com cobertura completa de todos os argumentos.
