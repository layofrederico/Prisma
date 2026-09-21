# Carrossel — Seu benefício fiscal entrou na conta da dívida

10 slides, **1080×1350** (4:5). Brand Prisma: fundo `#01066A`, texto branco, barra
gradiente do logo, Poppins, logo em círculo branco na capa e no CTA, handle
`@prismacontabilto` no rodapé. Público: empresário com benefício fiscal de ICMS.

## Roteiro

| # | Slide | Gancho |
|---|---|---|
| 01 | Capa | R$ 10,9 tri de dívida — e o seu benefício fiscal entrou na conta |
| 02 | O buraco | R$ 3,1 bi/dia de juros; R$ 96 bi/mês contra meta anual de R$ 34,3 bi |
| 03 | Três saídas | Cortar, crescer ou arrecadar — a mais rápida já está em curso |
| 04 | Onde está o dinheiro | Benefícios federais = 4,4% do PIB; Constituição manda reduzir a 2% |
| 05 | Data marcada | ICMS cai de 2029 a 2032; benefício calculado sobre ele cai junto |
| 06 | O fundo | Compensação existe, mas só para benefício **oneroso** |
| 07 | Os três filtros | Prazo e condição · concessão regular até 31/05/2023 · habilitação |
| 08 | O prazo | Habilitação até **31/12/2028**, sem segunda chance |
| 09 | O que fazer | Achar o ato, ler prazo e contrapartida, reunir prova |
| 10 | Chamada | Leitura do ato de concessão em uma reunião |

## Base normativa (verificada em 21/09/2026)

| Tema | Dispositivo | Marcação |
|---|---|---|
| Plano de redução de benefícios federais a 2% do PIB | art. 4º da EC nº 109/2021 | VERIFICADO |
| Gastos tributários federais: 4,40% do PIB em 2025 | Nota técnica conjunta do PLOA 2026 (Senado) | VERIFICADO |
| Renúncia exige estimativa e compensação | art. 14 da LC nº 101/2000 (LRF) | MEMÓRIA — conferir |
| Limite de despesa = 70% da variação da receita primária | LC nº 200/2023 | VERIFICADO |
| Transição do ICMS 2029–2032 e extinção em 2033 | EC nº 132/2023; art. 128 do ADCT | VERIFICADO (fonte secundária) |
| Fundo de Compensação de Benefícios Fiscais | art. 12 da EC nº 132/2023; arts. 125, §3º e 128 do ADCT; arts. 384 a 405 da LC nº 214/2025; Portaria RFB nº 635/2025 | VERIFICADO (fonte secundária) |
| Benefício oneroso, concedido regularmente até 31/05/2023 | LC nº 214/2025 | VERIFICADO (fonte secundária) |
| Habilitação de 01/01/2026 a 31/12/2028 | art. 388 da LC nº 214/2025 | VERIFICADO (fonte secundária) |

Conferir a redação consolidada no Planalto antes de orientar cliente por escrito;
a LC nº 214/2025 foi alterada pela LC nº 227/2026.

## Base macro (BCB e Tesouro, julho/2026)

| Dado | Valor |
|---|---|
| Dívida bruta (DBGG) | R$ 10,947 tri — 82,5% do PIB |
| Juros nominais 12 meses | R$ 1,15 tri (8,67% do PIB) |
| Resultado nominal 12 meses | −R$ 1,24 tri (−9,34% do PIB) |
| Resultado primário 12 meses | −R$ 89,3 bi (−0,67% do PIB) |
| Selic | 13,75% a.a. (Copom, 16/09/2026) |
| Pós-fixado à Selic | 51,11% da DPF |
| Meta primário 2026 | +0,25% do PIB (R$ 34,3 bi) |

```
R$ 1,15 tri ÷ 365 dias     = R$ 3,15 bi/dia   (slide 02)
R$ 1,15 tri ÷ 12 meses     = R$ 95,8 bi/mês   (slide 02)
```

Ajuste necessário para estabilizar a dívida: `Δd = [(i − g)/(1+g)] × d₋₁ − s`, com
i = 10,51% (8,67 ÷ 82,5), g = 6,60% (premissa) e d = 82,5% → superávit primário de
3,03% do PIB ≈ R$ 402 bi/ano. Confronto com os 4,4% do PIB de benefícios federais é
o que sustenta o slide 04. Teste de sanidade: o modelo projeta +3,70 p.p./ano contra
+3,9 p.p. observados pelo BC em 12 meses.

## Versão visual e animada (set/2026)

Cada slide passou a ter uma figura de dados em SVG, com objetos em movimento
(CSS): barras que crescem, a escada do ICMS caindo ano a ano, o fluxo da
bifurcação do fundo, o marcador "hoje" pulsando na régua do prazo.

Paleta de dados validada com `scripts/validate_palette.js` da skill dataviz
(modo dark, superfície `#01066A`) — 5 de 5 checks aprovados:

| Papel | Hex |
|---|---|
| Destaque / alerta | `#DE3A76` |
| Série principal | `#1B8CC8` |
| Comparação | `#B67D0A` |
| Positivo | `#159B70` |

O gradiente pastel do logo fica restrito a elemento decorativo (barras do
cabeçalho e do rodapé); dado nunca usa cor decorativa.

### Artboard interativo

`project/Quiz.dc.html` — triagem de onerosidade em três perguntas com botões,
resultado condicional e chamada para contato. Marcado com `is_interactive`.
Serve como página de link na bio; não vai para o feed como imagem.
