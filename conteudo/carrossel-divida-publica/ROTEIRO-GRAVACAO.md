# Roteiro de gravação — Reel da dívida pública

Sete falas, uma por slide. **94 palavras, 37,6 s de locução**; com as pausas de 1 s entre parágrafos e
1,5 s de tela parada no fim, o Reel fica com **cerca de 45 segundos**.

## Texto para gravar

Leia em voz alta, na ordem. **Pausa de 1 segundo entre um parágrafo e o outro** — é ela que marca a
troca de slide. As palavras em negrito são as que recebem ênfase.

> Hoje, cada brasileiro deve **cinquenta e um mil reais**. Inclusive quem acabou de **nascer**.
>
> A dívida nasceu com o país: em **mil oitocentos e vinte e quatro**, em Londres.
>
> O governo deve **dez vírgula nove trilhões**. Quase oitenta e três por cento do PIB.
>
> Mais de **três bilhões de juros por dia**. Um mês supera a meta anual.
>
> De cada cem reais que faltam, **noventa e três são juros**.
>
> Crédito, imposto, dólar e cliente sem dinheiro. Em cada porta, **dá para agir**.
>
> Quer saber quanto está **perdendo**? Comente **eu quero** e receba a calculadora.

## Direção de voz, fala por fala

| # | Slide | Entra em | Fala | Palavras | Como dizer |
|---|---|---|---|---|---|
| 01 | Cada brasileiro deve | 0:00 | 5,6 s | 14 | Tom de revelação. Micro-pausa antes de “Inclusive”; “nascer” cai, não sobe. |
| 02 | A dívida nasceu com o Brasil | 0:06 | 6,0 s | 15 | Narrativo, um pouco mais lento: é história. Pausa curta depois dos dois-pontos. |
| 03 | Gauge 82,5% | 0:13 | 6,0 s | 15 | Firme, sem dramatizar. Deixe o número respirar antes do “Quase”. |
| 04 | R$ 3,1 bi por dia | 0:20 | 5,6 s | 14 | Ritmo mais rápido em “três bilhões de juros por dia”; a segunda frase sai seca. |
| 05 | Quase tudo é juro | 0:27 | 4,4 s | 11 | A frase mais curta: pausa leve antes de “noventa e três”. |
| 06 | No seu caixa | 0:32 | 5,2 s | 13 | Enumere as quatro portas no mesmo ritmo; vire o tom em “dá para agir” — é a virada do vídeo. |
| 07 | Faça a sua conta | 0:38 | 4,8 s | 12 | Conversa direta com quem assiste, sorrindo. “Eu quero” bem destacado. |
| | **Total** | | **37,6 s** | **94** | + 6 pausas de 1 s + 1,5 s no fim ≈ **45 s** |

Tempo estimado a 2,5 palavras por segundo (150 por minuto), ritmo de locução institucional. O horário
de entrada de cada slide soma a fala anterior e a pausa de 1 s. No vídeo final, o corte segue as
pausas reais da sua gravação, não esta tabela.

## Como gravar

1. **Lugar silencioso**, sem ventilador nem ar-condicionado ligado. Quarto com cortina, armário ou
   sofá abafa o eco melhor que sala vazia.
2. **Celular a um palmo da boca**, um pouco abaixo do queixo, para não estourar o “p” e o “b”.
   O gravador de voz do celular serve.
3. **Dois segundos de silêncio antes de começar** e dois no fim.
4. **Pausa de 1 segundo entre parágrafos.** Dentro da frase, respire normalmente: pausas curtas não
   viram troca de slide.
5. **Errou? Recomece do primeiro parágrafo** numa nova gravação. Repetir só o trecho errado cria uma
   pausa a mais e desalinha os cortes, porque a montagem usa as pausas longas para trocar de slide.
6. Grave duas tomadas completas e mande a que soar mais natural (ou as duas).
7. **Formato:** m4a, mp3, wav ou áudio do WhatsApp — todos funcionam.

## O que acontece depois do envio

A montagem é automática (`video/monta-video.py`):

1. Detecta as seis pausas entre parágrafos e usa cada uma como corte de slide.
2. Renderiza as animações de cada slide no tempo exato da sua fala, a 30 quadros por segundo.
3. Aplica a legenda na tela (texto de `video/legendas-tela.json`) — a maioria assiste sem som.
4. Normaliza o volume em **−14 LUFS**, o padrão das redes.
5. Entrega o MP4 **1080×1920** pronto para postar.

Se o script não achar as seis pausas, ele avisa e basta regravar com pausas um pouco mais longas.

## Publicação

- **Capa do Reel:** quadro final do slide 01, com o R$ 51.104 parado.
- **Legenda do post:** a mesma do carrossel (`LEGENDA.md`), que termina em “Comente EU QUERO”.
- **Resposta no direct:** quem comentar recebe o link da calculadora (mensagem sugerida no
  cabeçalho da `LEGENDA.md`). Compartilhe a calculadora pelo menu **Share** antes de publicar — sem
  isso, o link não abre para quem recebe.
- **Trilha:** instrumental discreta, sem percussão marcada, em volume bem abaixo da voz.

## Observações de produção

- **Números por extenso na fala.** O texto traz “dez vírgula nove trilhões”, e não “R$ 10,9 tri”, de
  propósito: quem lê o símbolo tropeça. Na legenda da tela, os números aparecem em algarismos.
- **Arredondamentos da fala:** R$ 51.103,59 por pessoa vira “cinquenta e um mil”; R$ 10,947 tri vira
  “dez vírgula nove”; 82,5% do PIB vira “quase oitenta e três por cento”; R$ 1,15 tri por ano ÷ 365
  ≈ R$ 3,15 bi, que vira “mais de três bilhões por dia”; R$ 1,15 tri de juros ÷ R$ 1,24 tri de
  déficit nominal = 92,8%, que vira “noventa e três”. Os valores exatos e as fontes estão nos slides.
- **Carrossel e Reel usam o mesmo texto:** as sete falas são o fio do carrossel, e a ordem dos
  slides é a mesma.
