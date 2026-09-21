# Carrossel — A dívida do governo no caixa da sua empresa

10 slides, **1080×1350** (4:5), identidade da Prisma Contábil: fundo `#01066A`,
texto branco, barra gradiente do logo, handle `@prismacontabilto` no rodapé, Poppins.
Público-alvo: empresário. Data-base dos dados: **julho/2026**.

## Roteiro

| # | Slide | Gancho |
|---|---|---|
| 01 | Capa | R$ 10,9 tri — e a conta chega na sua empresa |
| 02 | Juros por dia | R$ 3,1 bi/dia; R$ 96 bi/mês contra meta anual de R$ 34,3 bi |
| 03 | De onde vem o rombo | De cada R$ 100 que faltam, R$ 93 são juros |
| 04 | O piso do crédito | Governo paga 13,75% sem risco — por que o banco te cobraria menos? |
| 05 | No seu extrato | Recebível, giro, financiamento, venda parcelada |
| 06 | A conta que falta | Precisaria sobrar R$ 400 bi/ano; hoje falta |
| 07 | Três saídas | Cortar, crescer ou arrecadar — a mais rápida é arrecadar |
| 08 | O que vem aí | Revisão de benefícios, fim de desonerações, fiscalização mais fina |
| 09 | Três perguntas | Indexação do passivo, prazo do benefício, custo do parcelamento |
| 10 | Chamada | Fale com um contador |

## Base numérica (verificada em 21/09/2026)

| Dado | Valor | Fonte |
|---|---|---|
| Dívida bruta (DBGG) | R$ 10,947 tri — 82,5% do PIB | BCB, Estatísticas Fiscais jul/2026 |
| Juros nominais 12 meses | R$ 1,15 tri (8,67% do PIB) | BCB |
| Resultado nominal 12 meses | −R$ 1,24 tri | BCB |
| Resultado primário 12 meses | −R$ 89,3 bi | BCB |
| Selic | 13,75% a.a. | Copom, 16/09/2026 |
| Pós-fixado à Selic | 51,11% da DPF | Tesouro, RMD jul/2026 |
| Meta primário 2026 | +0,25% do PIB (R$ 34,3 bi) | LDO 2026 / LC 200/2023 |

Derivações usadas nos slides:

```
R$ 1,15 tri ÷ 365 dias          = R$ 3,15 bi/dia      (slide 02)
R$ 1,15 tri ÷ 12 meses          = R$ 95,8 bi/mês      (slide 02)
R$ 1,15 tri ÷ R$ 1,24 tri       = 92,7% → R$ 93/100   (slide 03)
```

Superávit estabilizador (slide 06): `Δd = [(i − g)/(1+g)] × d₋₁ − s`, com
i = 10,51% (8,67 ÷ 82,5), g = 6,60% (premissa) e d = 82,5% → s* = 3,03% do PIB
≈ **R$ 402 bi/ano** sobre PIB nominal implícito de R$ 13,27 tri (10,947 ÷ 0,825).
Teste de sanidade: o modelo projeta +3,70 p.p./ano contra +3,9 p.p. observados
pelo BC em 12 meses.

> A memória de cálculo fica fora do carrossel de propósito — ela é o lastro da
> peça, não o conteúdo. Vale como material de apoio para stories, comentários
> ou uma versão longa no LinkedIn.
