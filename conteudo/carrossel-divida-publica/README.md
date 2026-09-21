# Carrossel — A dívida do Brasil lida como balanço

Peça de 10 slides (1080×1080) para Instagram/LinkedIn. Data-base dos dados: **julho/2026**;
posição da pesquisa: **21/09/2026**. Canvas editável publicado como Artifact (link na sessão).

## Fontes

| Dado | Valor | Fonte | Marcação |
|---|---|---|---|
| DBGG jul/2026 | R$ 10,947 tri — 82,5% do PIB | BCB, Estatísticas Fiscais (31/08/2026) | VERIFICADO |
| Variação 12 meses | +3,9 p.p. do PIB | BCB | VERIFICADO |
| Primário 12 meses | −R$ 89,3 bi (−0,67% do PIB) | BCB | VERIFICADO |
| Juros nominais 12 meses | −R$ 1,15 tri (−8,67% do PIB) | BCB | VERIFICADO |
| Nominal 12 meses | −R$ 1,24 tri (−9,34% do PIB) | BCB | VERIFICADO |
| DPF jul/2026 | R$ 9,298 tri | Tesouro Nacional, RMD jul/2026 | VERIFICADO |
| Pós-fixado Selic | 51,11% da DPF | Tesouro Nacional, RMD | VERIFICADO |
| Custo médio DPF 12 m | 12,4% | Tesouro Nacional, RMD | VERIFICADO |
| Selic | 13,75% a.a. | Copom, 16/09/2026 | VERIFICADO |
| Meta primário 2026 | +0,25% do PIB (R$ 34,3 bi) | LDO 2026 / LC 200/2023 | VERIFICADO |
| PIB nominal implícito | R$ 13,27 tri | 10,947 ÷ 0,825 | INFERÊNCIA |
| Juro implícito (i) | 10,51% a.a. | 8,67 ÷ 82,5 | INFERÊNCIA |
| PIB nominal (g) | 6,60% a.a. | premissa do autor | PREMISSA |

## Memória de cálculo

Dinâmica da dívida: `Δd = [(i − g)/(1 + g)] × d₋₁ − s`

```
(0,1051 − 0,0660) ÷ 1,0660 = 0,036679
0,036679 × 0,825            = 0,030260
0,030260 + 0,006700         = 0,036960  →  +3,70 p.p. do PIB/ano
```

Superávit estabilizador: `s* = 0,030260` → **3,03% do PIB** ≈ R$ 402 bi/ano.
Esforço sobre o resultado corrente: 3,70 p.p. ≈ R$ 491 bi/ano.

Teste de sanidade: variação observada pelo BC em 12 meses = +3,9 p.p. (desvio de 0,2 p.p.).

Sensibilidade (variação isolada de g, com i = 10,51% e s = −0,67%):

| PIB nominal | Δ dívida/PIB ao ano |
|---|---|
| 5,00% | +5,00 p.p. |
| 6,60% | +3,70 p.p. |
| 8,00% | +2,59 p.p. |

Elasticidade ao custo: cada −1 p.p. em `i` reduz Δd em 0,77 p.p. do PIB ao ano.

## Arquivos

`project/` contém o índice do canvas (`canvas.json`) e um arquivo `.dc.html` por slide,
na ordem de publicação: Main, Passivo, DRE, Cobertura, Indexacao, Equacao, Calculo,
Ajuste, Sensibilidade, Aplicacao.
