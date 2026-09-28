# Post — código de autenticidade do comprovante do CNPJ

Carrossel de 5 cards 4:5 (1080×1350) no kit visual da Prisma e legenda para o Instagram. As imagens são
recortes do Modelo II publicado no DOU; nenhum campo foi redesenhado.

| Card | Arquivo | Conteúdo |
|---|---|---|
| 01 | `project/Main.dc.html` | O que é: a linha "Código de autenticidade" do Modelo II |
| 02 | `project/Onde.dc.html` | Onde aparece: só no Modelo II, na última linha |
| 03 | `project/Conteudo.dc.html` | O que mais vem no Modelo II: representante legal, quadro de sócios, quem emitiu |
| 04 | `project/Conferir.dc.html` | Como conferir: frase do modelo e caminho da validação no gov.br |
| 05 | `project/Usar.dc.html` | Quando usar (orientação da Prisma) e "Salve este post" |

- `legenda-instagram.txt`: legenda pronta para colar.
- `gera-autentic.py`: gera os cards; depende de `gera-cnpj2.py` (post do novo comprovante).

## Base [VERIFICADO em 28/09/2026]

- **Anexo Único da IN RFB nº 2.345/2026** (DOU de 23/09/2026), Modelo II:
  - "Código de autenticidade: <NnaNNNaNNNaaaNNN>";
  - "O código pode ser consultado no endereço <https://www.redesim.gov.br>";
  - "Emitido no dia xx/xx/xxxx às xx:xx:xx (data e hora de Brasília) por <nome do usuário logado> - CPF xxx.xxx.xxx-xx";
  - "Informações vigentes na data da emissão".

  O Modelo I não tem código de autenticidade.
- **IN RFB nº 2.119/2022, art. 10:** o comprovante tem os modelos I e II, que constam do Anexo III. O
  parágrafo único diz que os modelos podem ser acessados na página da RFB ou no Portal Redesim.
- **gov.br › Empresas e Negócios › Redesim:**
  - Comprovantes: "Emitir Comprovante de Inscrição com Código de Autenticidade";
  - Validação: "Validar Comprovante de Inscrição — Confirme a autenticidade de Comprovante de
    Inscrição e Situação Cadastral no CNPJ", em <https://consultacnpj.redesim.gov.br/autenticidade-comprovante-inscricao>.

## Não entrou no post

Quem pode emitir o Modelo II e desde quando ele existe (a Receita divulgou em 2020, com a
IN RFB nº 1.963/2020) ficaram de fora. A notícia oficial exige login no gov.br e não pôde ser lida
na íntegra nesta sessão. Os campos que o validador da Redesim pede também ficaram de fora, porque a
página não abriu aqui.
