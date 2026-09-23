---
name: painel-gerencial-mensal
description: Procedimento padrão da Prisma Contábil para o painel gerencial mensal de cliente — consolida balancete e DRE exportados do Domínio Contábil, valida integridade, calcula KPIs, explica variações (real × orçado, mês × mês, ano × ano) e entrega o painel em XLSX, PDF ou artefato no formato KPIs → fatores de variação → riscos → ações. Use quando o pedido envolver painel, dashboard, relatório gerencial, fechamento mensal, comentário de DRE, análise de variação, KPIs, indicadores de liquidez, margem, ciclo de caixa ou carga tributária efetiva de um cliente, ainda que sem citar a palavra "painel".
---

# Painel gerencial mensal — Prisma Contábil

Fluxo único para transformar o fechamento contábil de um cliente em painel executivo auditável. Vale para qualquer entrega (XLSX, PDF, artefato HTML ou PPTX); o formato de saída é escolhido no passo 6.

## 0. Pré-requisitos e sigilo

- Base do cliente pseudonimizada antes do processamento: substituir razão social por código (`CLI-001`), remover CPF de sócios e dados de empregados (LGPD, Lei nº 13.709/2018, art. 6º, I e III — finalidade e necessidade).
- Identificar: regime tributário (Simples, Presumido, Real), atividade (CNAE principal), competência analisada (`MM/AAAA`) e comparativos disponíveis (mês anterior, mesmo mês do ano anterior, orçamento).

## 1. Entrada de dados

Arquivos esperados, normalmente exportados do Domínio Contábil (confirmar o caminho de menu na versão instalada — varia por release):

| Arquivo | Conteúdo mínimo | Uso |
|---|---|---|
| Balancete de verificação (XLS/CSV) | conta, descrição, nível, saldo anterior, débitos, créditos, saldo atual | Balanço, liquidez, ciclo de caixa |
| DRE do período e acumulada | linhas da DRE com valores do mês e acumulado | Margens, variações |
| Orçamento (opcional) | mesmas linhas da DRE por competência | Real × orçado |
| Razão de contas selecionadas (opcional) | lançamentos das contas com maior variação | Rastrear causa da variação |

Leitura: CSV/TXT legado do Domínio costuma vir em `cp1252` — ler com fallback (`utf-8-sig` → `cp1252` → `latin-1`) e registrar o encoding usado. Delimitador `;`, decimal `,`.

## 2. Validação de integridade (bloqueante)

Nenhum KPI é calculado antes de todos os testes abaixo passarem ou de a divergência ser reportada ao usuário.

1. **Partidas dobradas**: $\sum \text{Débitos} = \sum \text{Créditos}$ no balancete (tolerância zero; divergência de centavos é reportada, não absorvida).
2. **Equação patrimonial**: $\text{Ativo} = \text{Passivo} + \text{PL}$ (com o resultado do período incorporado ao PL se ainda não encerrado).
3. **Amarração DRE × balancete**: soma das contas de resultado do balancete = lucro/prejuízo da DRE.
4. **Continuidade**: saldo anterior do mês = saldo atual do mês anterior (quando houver os dois balancetes).
5. **Contas com saldo invertido**: caixa/bancos credores, fornecedores devedores, estoques negativos — listar como alerta.
6. **Registros rejeitados**: linhas não lidas ou sem conta válida são contadas e listadas; nunca descartadas em silêncio.

Registrar o resultado em um bloco "Controles" (teste, valor esperado, valor obtido, status).

## 3. KPIs padrão

Calcular apenas os que os dados suportam; declarar os omitidos e por quê. Toda fórmula sai em LaTeX com a origem de cada variável (conta ou linha da DRE).

| Grupo | KPI | Fórmula |
|---|---|---|
| Receita | Receita líquida; variação % | $\Delta\% = \frac{RL_t - RL_{t-1}}{RL_{t-1}} \times 100$ |
| Rentabilidade | Margem bruta; margem EBITDA; margem líquida | $MB = \frac{\text{Lucro bruto}}{RL} \times 100$ |
| Liquidez | Liquidez corrente; liquidez seca; liquidez imediata | $LC = \frac{AC}{PC}$ |
| Ciclo | PMR, PME, PMP; ciclo de caixa | $CC = PMR + PME - PMP$, com $PMR = \frac{\text{Clientes}}{\text{Receita bruta}} \times \text{dias}$ |
| Estrutura | Endividamento geral; composição do endividamento | $EG = \frac{PC + PNC}{\text{Ativo total}}$ |
| Tributos | Carga tributária efetiva sobre a receita | $CTE = \frac{\text{Tributos sobre receita + IRPJ/CSLL}}{\text{Receita bruta}} \times 100$ |

Regras: percentual com 2 casas, arredondamento meio para cima (NBR 5891); divisão por zero ou base negativa → "n/a" com nota; dias do período declarados (30 ou dias corridos da competência).

## 4. Análise de variação

Para cada linha da DRE e cada KPI: variação absoluta (R$) e relativa (%), contra cada comparativo disponível.

- **Materialidade**: comentar só variações acima de **5%** *e* acima de **R$ 5.000,00** (limiares ajustáveis por cliente; declarar os usados).
- Ordenar pelas maiores variações absolutas; no máximo 5 fatores no painel.
- Para cada fator, rastrear a causa no razão (conta, lançamentos relevantes, histórico) — sem causa identificada, escrever "causa não identificada nos dados; confirmar com o cliente", nunca inventar explicação.
- Sazonalidade: quando houver 12+ competências, comparar também com o mesmo mês do ano anterior antes de chamar a variação de anomalia.

## 5. Estrutura narrativa do painel

Sempre nesta ordem, em linguagem executiva (conselho/sócio):

1. **KPIs** — 4 a 6 cartões: valor, variação e seta; data-base "posição em dd/mm/aaaa".
2. **Fatores de variação** — até 5 itens: o que mudou, quanto (R$ e %), por quê (conta de origem).
3. **Riscos** — sinalizar exposição fiscal (ex.: carga efetiva fora do padrão do regime), trabalhista, de liquidez (LC < 1, ciclo de caixa em alta) e de qualidade da informação (controles do passo 2 com alerta).
4. **Ações** — recomendações operacionais com responsável sugerido e prazo.

Comentário de DRE: uma frase por linha material, iniciando pelo número ("Despesas administrativas subiram R$ 12.340,00 (+18,20%), concentradas em …").

## 6. Formato de saída

- **XLSX** (usar a skill `xlsx`): abas `Painel`, `DRE`, `Balanço`, `KPIs`, `Variações`, `Controles`, `Premissas`. Fórmulas vivas, não valores colados; `numFmt` monetário `'[$R$-416] #,##0.00'`; percentuais `0.00%`; área de impressão A4 paisagem na aba `Painel`; linha de total com conferência de soma.
- **PDF** (skill `pdf`) ou **PPTX** (skill `pptx`): uma página/slide por bloco do passo 5.
- **Artefato HTML**: cartões de KPI + gráficos (skill `dataviz`); nunca publicar dado real de cliente sem pseudonimização.
- CSV auxiliar: `;`, decimal `,`, UTF-8 com BOM.

## 7. Auditoria final antes de entregar

- Soma das partes = total em todas as tabelas.
- Cada número do painel rastreável até conta/linha de origem (aba `Premissas` ou nota de rodapé).
- Nenhuma fórmula com `#REF!`, `#VALOR!`, `#DIV/0!` ou referência circular.
- Data-base, regime tributário e limiares de materialidade declarados.
- Formato numérico brasileiro em todo o documento.
