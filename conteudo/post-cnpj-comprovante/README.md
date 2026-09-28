# Post — novo comprovante do CNPJ (IN RFB nº 2.345/2026)

Carrossel de 6 cards 4:5 (1080×1350) no kit visual da Prisma e legenda para o Instagram. Tudo o que o
post afirma sai do texto da IN e do seu Anexo Único, publicados no DOU de 23/09/2026. As imagens são
recortes do anexo oficial, sem redesenho.

| Card | Arquivo | Conteúdo |
|---|---|---|
| 01 | `project/Main.dc.html` | Capa: Modelo I inteiro, como publicado, e vigência (art. 2º) |
| 02 | `project/Datas.dc.html` | Antes e depois: DATA DE ABERTURA (Anexo III original da IN RFB nº 2.119/2022) → DATA DE INSCRIÇÃO NO CNPJ e DATA DE CONSTITUIÇÃO (IN RFB nº 2.345/2026) |
| 03 | `project/Codigos.dc.html` | Campos CÓDIGO QR e CÓDIGO DE BARRAS (recorte do Modelo I) |
| 04 | `project/ModeloII.dc.html` | Modelo II: representante legal, quadro de sócios e administradores, código de autenticidade |
| 05 | `project/Norma.dc.html` | Arts. 1º e 2º transcritos e fundamentos citados na IN |
| 06 | `project/Acao.dc.html` | O que conferir e chamada "Salve este post" |

## Story com enquete (pasta `story/`)

Sequência de dois stories para levar ao Reel:

1. `story-cnpj.mp4` (10 s, animado) ou `story-cnpj.png` (estático), 1080×1920: pergunta "Você já viu o
   novo comprovante do CNPJ?", o Modelo I do anexo e uma área livre para a enquete do Instagram
   ("Sim, já vi" / "Ainda não"). `story-cnpj-guia.png` mostra onde encaixar a enquete e não deve ser
   publicado. As faixas de 0 a 220 px e de 1720 a 1920 px ficam livres para a interface do Instagram.
2. O próprio Reel compartilhado no story (avião de papel → Adicionar ao story).

`story-cnpj.html` é a página de origem; renderizada pelo `renderiza.js` do pipeline de vídeo.

## Reel

`reel-cnpj.py` gera `reel-cnpj.mp4` (1080×1920, 64,9 s) e `reel-cnpj.srt`. Cada card dura o tempo da
sua fala (2,5 palavras/s) + 0,4 s de entrada + 1,0 s de respiro, com mínimo de 5 s. A fala aparece na
tela e vai para o SRT com os mesmos tempos. A vinheta da Prisma fecha o vídeo.

| # | Card | Card (s) | Fala no SRT (s) |
|---|---|---|---|
| 1 | Capa com o Modelo I | 0,0–5,9 | 0,4–4,8 |
| 2 | Antes e depois | 5,9–14,9 | 6,3–13,9 |
| 3 | Código QR e de barras | 14,9–23,9 | 15,3–22,9 |
| 4 | Modelo II | 23,9–30,9 | 24,3–29,9 |
| 5 | Texto da IN | 30,9–38,7 | 31,3–37,7 |
| 6 | O que a IN não exige | 38,7–45,3 | 39,1–44,3 |
| 7 | Cadastro único da reforma | 45,3–51,5 | 45,7–50,5 |
| 8 | O que conferir | 51,5–59,3 | 51,9–58,3 |
| — | Vinheta (fusão de 0,5 s) | 58,8–64,9 | — |

## Texto da norma (DOU de 23/09/2026) [VERIFICADO]

Fonte: <https://www.in.gov.br/web/dou/-/instrucao-normativa-rfb-n-2.345-de-22-de-setembro-de-2026-733661854>

> Altera a Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, para adequar o Comprovante de
> Inscrição e de Situação Cadastral às alterações promovidas no Cadastro Nacional da Pessoa Jurídica.
>
> Art. 1º O Anexo III da Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, denominado
> Comprovante de Inscrição e de Situação Cadastral, fica substituído pelo Anexo Único desta
> Instrução Normativa.
>
> Art. 2º Esta Instrução Normativa entra em vigor na data de sua publicação no Diário Oficial da União.

Fundamentos citados no preâmbulo: art. 350, III, do Regimento Interno da RFB (Portaria ME nº 284/2020);
Portaria MF nº 220/2026; Lei nº 5.614/1970; art. 59 da LC nº 214/2025; arts. 104 e 105 do Decreto
nº 12.955/2026.

Anexo Único:
- **Modelo I**, rodapé "Emitido no dia XX/XX/XXXX às XX:XX:XX (data e hora de Brasília)".
- **Modelo II**, "Informações vigentes na data da emissão", rodapé "Emitido no dia xx/xx/xxxx às
  xx:xx:xx (data e hora de Brasília) por <nome do usuário logado> - CPF xxx.xxx.xxx-xx" e "O código
  pode ser consultado no endereço <https://www.redesim.gov.br>".

## O que ficou fora do post, por não estar na norma

A primeira versão, feita com base em notícias, trazia afirmações que a IN não contém. Foram
retiradas (a troca da "data de abertura" voltou depois, confirmada pela comparação com o Anexo III
original publicado no DOU; ver abaixo):
- "página única";
- CNPJ alfanumérico desde 31/07/2026;
- "não há recadastramento";
- "o comprovante antigo continua válido".

Algumas notícias também diziam que o Modelo II foi eliminado. O anexo publicado traz o Modelo II.

## Comparação com o modelo original da IN RFB nº 2.119/2022 [VERIFICADO no DOU]

Imagens em `anexo/in2119-2022-*.jpg`, baixadas da publicação original da IN RFB nº 2.119/2022 (DOU de
08/12/2022). A comparação é com essa versão original: se o Anexo III foi alterado entre 2022 e 2026 por
outra IN, essa alteração intermediária não foi verificada.

| Item | Anexo III original (2022) | Anexo Único da IN RFB nº 2.345/2026 |
|---|---|---|
| Campo de data no topo | DATA DE ABERTURA | DATA DE INSCRIÇÃO NO CNPJ |
| Data de constituição | Não havia | DATA DE CONSTITUIÇÃO |
| Código QR e código de barras | Não havia | Nos Modelos I e II |
| Código de autenticidade no modelo | Não aparecia | Modelo II: "Código de autenticidade" e "O código pode ser consultado no endereço https://www.redesim.gov.br" |
| Nota sobre dispensa de alvarás e licenças (Resolução CGSIM nº 51/2019) | Nota (*) no rodapé dos dois modelos | Não aparece |
| Rodapé de emissão | Não havia | Data e hora de emissão; no Modelo II, também o usuário logado e o CPF |

O Anexo II da IN RFB nº 2.119/2022 é outro documento: o "Protocolo de Transmissão do CNPJ" (Protocolo
Redesim), previsto no art. 13, que não foi alterado pela IN RFB nº 2.345/2026.
