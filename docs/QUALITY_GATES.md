# Quality Gates — googlesearch

Critérios de validação por fase do protocolo AES. Um task só está "feito" quando todos os gates aplicáveis passam.

## Fase 0 — Reconhecimento (obrigatório antes de qualquer código)
- [ ] `make wake` executado (INDEX.md lido, acessos a shadow docs registados em `aes/shadow/access.log`)
- [ ] Ficheiros diretamente afetados lidos e padrões de código identificados
- [ ] Testes existentes para os ficheiros afetados identificados
- *Saída:* hostil analysis documentado (assumptions, alternativas, riscos, custo de estar errado)

## Fase 1 — Hostile Analysis (obrigatório)
- [ ] Assumptions classificadas: [KNOWN] / [INFERRED] / [ASSUMED] / [UNKNOWN]
- [ ] "What wasn't specified" preenchido
- [ ] Alternativas não escolhidas listadas com justificação
- [ ] Risks & side effects identificados
- [ ] Cost of being wrong: low / medium / high (com justificação)
- *Gate:* se cost = HIGH → pausar e confirmar com o utilizador antes de prosseguir

## Fase 2 — Solution Proposal
- [ ] Abordagem escolhida declarada claramente
- [ ] O que será alterado e o que não será alterado (e porquê)
- [ ] Critérios de verificação: como se sabe que funcionou?

## Fase 3 — Implementation
- [ ] Diff mínimo, sem código morto, sem blocos comentados
- [ ] Cada nova função tem docstring ou comentário a explicar *porquê*, não *o quê*
- [ ] Sem scope creep (descobertas fora de scope vão para `docs/ROADMAP.md` com tag `[DISCOVERED mid-task]`)

## Fase 4 — Validation
| Gate | Comando | Bloqueia se falhar? |
|------|---------|---------------------|
| Testes | `make test` | Sim (novas falhas) |
| Lint | `make lint` | Sim (novos erros) |
| Formato | `ruff format --check googlesearch/ tests/` | Sim |
| Importação pública | `python -c "from googlesearch import search, lucky, get_tbs, get_random_user_agent, filter_result"` | Sim |
| `setup.py` | `python ./setup.py --name` | Sim |

**Regras de falha:**
- Teste novo a falhar → NÃO prosseguir. Corrigir ou reverter.
- Falha pré-existente → reportar, não bloquear.
- Lint novo → NÃO prosseguir.
- Docs em falta → NÃO prosseguir. Criar primeiro.
- Erro de ambiente (dependência em falta, permissão) → não contornar silenciosamente. Reportar e parar.

## Fase 5 — Critical Review
- [ ] Pode ser mais simples? (se sim → simplificar)
- [ ] Correto para todos os inputs identificados?
- [ ] Introduz dívida técnica? (se sim → criar task para ela)
- [ ] Um colega entenderia sem perguntar?
- [ *] Insight valioso para `docs/HOSTILE_INSIGHTS.md`?

## UX Manifests (UI projects)
Não aplicável — `googlesearch` é uma biblioteca Python sem UI. Os gates FC-1 a FC-9 passam silenciosamente (não existe `docs/UX/pages/`).

## Pre-commit (quick checklist)
- [ ] Testes passam
- [ ] Lint passa
- [ ] Formato correto
- [ ] Sem `console.log`/debug no source
- [ ] Sem `TODO` no source
- [ ] Docs atualizados (se comportamento mudou)
- [ ] Diffstory escrito

## Pre-release (thorough checklist)
Ver `docs/CHECKLIST.md` para itens específicos de domínio.
