# Post — novo comprovante do CNPJ (IN RFB nº 2.345/2026)

Carrossel de 6 cards 4:5 (1080×1350) no kit visual da Prisma e legenda para o Instagram. Tudo o que o
post afirma sai do texto da IN e do seu Anexo Único, publicados no DOU de 23/09/2026. As imagens são
recortes do anexo oficial, sem redesenho.

| Card | Arquivo | Conteúdo |
|---|---|---|
| 01 | `project/Main.dc.html` | Capa: Modelo I inteiro, como publicado, e vigência (art. 2º) |
| 02 | `project/Datas.dc.html` | Campos DATA DE INSCRIÇÃO NO CNPJ e DATA DE CONSTITUIÇÃO (recorte do Modelo I) |
| 03 | `project/Codigos.dc.html` | Campos CÓDIGO QR e CÓDIGO DE BARRAS (recorte do Modelo I) |
| 04 | `project/ModeloII.dc.html` | Modelo II: representante legal, quadro de sócios e administradores, código de autenticidade |
| 05 | `project/Norma.dc.html` | Arts. 1º e 2º transcritos e fundamentos citados na IN |
| 06 | `project/Acao.dc.html` | O que conferir e chamada "Salve este post" |

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

A primeira versão, feita com base em notícias, trazia afirmações que a IN não contém. Todas foram
retiradas:
- "data de abertura" substituída;
- "página única";
- CNPJ alfanumérico desde 31/07/2026;
- "não há recadastramento";
- "o comprovante antigo continua válido".

Algumas notícias também diziam que o Modelo II foi eliminado. O anexo publicado traz o Modelo II.
