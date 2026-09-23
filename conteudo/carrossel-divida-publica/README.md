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

## Roteiro vigente — a dívida como tema (set/2026)

| # | Slide | Gancho |
|---|---|---|
| 01 | Capa | R$ 10,9 trilhões · 82,5% do PIB, maior nível em 5 anos |
| 02 | A velocidade | 78,6% → 82,5% do PIB em doze meses (+3,9 p.p.) |
| 03 | Juros por dia | R$ 3,1 bi/dia; um mês de juros contra a meta de economia do ano |
| 04 | Quase tudo é juro | R$ 93 de cada R$ 100 que faltam |
| 05 | Metade pós-fixada | 51,11% da DPF acompanha a Selic; 1 p.p. reprecifica R$ 4,75 tri |
| 06 | Por que cresce | Juro implícito 10,5% contra PIB nominal 6,6% |
| 07 | Meta × conta | R$ 402 bi necessários contra R$ 34,3 bi de meta |
| 08 | No seu caixa | Selic 13,75% como piso do crédito: recebível, giro, financiamento, parcelamento |
| 09 | Benefício na mira | 4,4% do PIB em benefícios; lei manda reduzir a 2% |
| 10 | Chamada | Fale com um contador |

Artboard extra `Quiz.dc.html` (fora dos dez): triagem interativa de onerosidade
de benefício de ICMS, para uso como página de link na bio.

### Divergência de fonte a conferir

A matéria secundária sobre o RMD de julho/2026 reporta a composição da DPF como
Selic 51,11%, índices de preços 25,90%, prefixados 21,04% e câmbio 3,74% — soma
de **101,79%**, portanto inconsistente. Por isso o slide 05 usa apenas o recorte
"51,11% pós-fixado contra 48,89% do restante", que não depende da abertura
completa. Conferir a composição no Relatório Mensal da Dívida original
(tesourotransparente.gov.br) antes de publicar a abertura em quatro fatias.

### Pendência resolvida — conferência no relatório oficial (23/09/2026)

Conferido direto no Relatório Mensal da Dívida de julho/2026 (Tesouro Nacional, tabelas 2.3 e 4.1):

| Indexador | Jun/26 | Jul/26 |
|---|---|---|
| Taxa flutuante (Selic) | 49,32% | **51,11%** |
| Índices de preços | 25,90% | **26,02%** |
| Prefixado | 21,04% | **19,22%** |
| Câmbio | 3,74% | **3,65%** |
| **Total** | 100,00% | **100,00%** |

A soma de 101,79% da fonte secundária vinha de misturar os 51,11% de julho com os
percentuais de junho. Estoque da DPF em julho: R$ 9.288,78 bi; em taxa flutuante,
R$ 4.747,25 bi (o "R$ 4,75 tri" do slide confere). Custo médio da DPF em 12 meses:
**12,45% a.a.** (a fonte secundária arredondou para 12,4%).

### Slide "Por que cresce" — premissa trocada por dado oficial

A versão anterior mostrava 10,5% (juro implícito estimado) contra 6,6% (premissa de PIB
nominal), sem nota. Substituído por comparação real contra real, só com dados oficiais:

```
juro real da dívida = (1 + 12,45%) / (1 + 4,44%) − 1 = 7,67%  → exibido 7,7%
crescimento real    = 1,9% (PIB, quatro trimestres até jun/2026, IBGE)
razão               = 7,67 / 1,9 = 4,0 vezes
```

Fontes: Tesouro Nacional (RMD jul/2026, tabela 4.1), IBGE (IPCA de 12 meses até jul/2026:
4,44%; PIB do 2º trimestre de 2026).

### Slide da balança removido (23/09/2026)

O slide comparava o superávit necessário para estabilizar a dívida com a meta de 2026. O
valor necessário é saída de modelo e muda conforme a taxa usada: R$ 402 bi com o juro
implícito das estatísticas fiscais, cerca de R$ 620 bi com o custo médio oficial da dívida
federal. Como não é dado publicado e a mesma mensagem já está no slide "R$ 3,1 bi por dia"
(um mês de juros supera a meta do ano), o slide saiu. O carrossel passa a ter dez slides,
todos com dado oficial ou conta direta sobre dado oficial.
