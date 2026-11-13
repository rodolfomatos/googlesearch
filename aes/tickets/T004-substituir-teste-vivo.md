---
ticket: T004
title: Substituir teste ao vivo por fixture HTML estático
sprint: sprint-01
priority: high
status: done
created: 2026-11-13
---

# T004 — Substituir teste ao vivo por fixture HTML estático

## Contexto
O teste `test_returns_none_for_empty` na classe `TestLucky` (linha 70-72 do `tests/test_search.py`) faz um HTTP real ao Google:
```python
result = lucky(query="a9f3b7c2d8e1f4a6b0c3d2e1f4a5b6c7")
self.assertIsNone(result)
```
Este teste é não-determinístico: depende da rede, da disponibilidade do Google, e do HTML retornado. Se o Google estiver fora ou mudar, o suite fica vermelho sem ser culpa do código.

No T002 foi adicionada a classe `TestSearchOfflineLucky` com `test_lucky_returns_none_for_empty` que usa mock, mas o teste original `TestLucky.test_returns_none_for_empty` ainda faz HTTP real.

## Critérios de aceitação
- [ ] `TestLucky.test_returns_none_for_empty` modificado para usar `unittest.mock.patch` de `googlesearch.get_page` com fixture HTML vazio
- [ ] Zero testes no suite fazem HTTP real ao Google
- [ ] `make test` passa em ambiente offline (sem rede)
- [ ] `make lint` passa
- [ ] Ticket marcado como done no kanban
- [ ] Commit e push para origin/master

## Escopo
**Em scope:** `tests/test_search.py` (modificar `TestLucky.test_returns_none_for_empty`).
**Fora de scope:** qualquer outro ficheiro.

## Dependências
T002 (já concluído — estabeleceu fixtures HTML e padrão de mock).

## Rollback
Reverter a alteração em `TestLucky.test_returns_none_for_empty` para a versão original com HTTP real.

## Riscos conhecidos
- Remover o teste ao vivo significa que não validamos contra o Google real. Mitigação: o teste `test_returns_none_for_empty` original já usava uma query inexistente, que não testa comportamento real do Google de forma significativa.

## Notas
Ticket do backlog do sprint-01. Após este ticket, todo o suite de testes será 100% offline.
