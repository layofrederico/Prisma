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

`reel-cnpj.py` gera `reel-cnpj.mp4` (1080×1920, sem voz): cada card entra com a legenda na tela e a
vinheta da Prisma fecha o vídeo. Reaproveita `converte.py` e `monta-video.py` do Reel da dívida
pública; no Reel o "Arraste para o lado" sai.

| Card | Dura (s) | Legenda na tela |
|---|---|---|
| 01 Capa | 8,0 | A Receita publicou um novo modelo do comprovante do CNPJ. |
| 02 Duas datas | 9,0 | Ele traz a data de inscrição no CNPJ e a data de constituição. |
| 03 Códigos | 8,0 | No rodapé, código QR e código de barras. |
| 04 Modelo II | 11,0 | O Modelo II inclui representante legal, sócios e código de autenticidade. |
| 05 Texto da IN | 13,0 | A IN RFB nº 2.345/2026 vale desde 23/09/2026. |
| 06 O que conferir | 10,0 | Salve e confira o comprovante da sua empresa. |
| Vinheta (fusão 0,5 s) | 6,1 | — |
| **Total** | **64,6** | |

- `anexo/anexo-modelo1.jpg` e `anexo/anexo-modelo2.jpg`: Modelos I e II do Anexo Único, baixados do DOU.
- `legenda-instagram.txt`: legenda pronta para colar.
- `gera-cnpj2.py`: gera os cards; reaproveita os estilos do gerador do carrossel da dívida pública.

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
