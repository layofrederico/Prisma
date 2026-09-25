# Montagem do vídeo com a voz gravada

1. `transcreve.py <audio> <saida.json>` transcreve a locução palavra a palavra (faster-whisper, modelo
   `medium`, pt-BR) para conferir o texto lido e procurar vícios de fala ("é", "hã") e frases repetidas.
2. `edita-audio.py <audio> <saida.wav>` limpa a voz: filtro passa-alta de 80 Hz, corte do silêncio do
   início e do fim, pausas dentro da frase acima de 0,25 s encurtadas para 0,22 s e as 6 pausas entre
   os 7 parágrafos padronizadas em 0,60 s. Cada emenda leva 12 ms de cross-fade, sem estalo. O log
   lista cada pausa com a duração original e a final.
3. `converte.py` transforma cada slide `.dc.html` numa página 1080×1920 (slide 4:5 no alto, legenda
   embaixo) com `window.__setTime(t)`, que posiciona todas as animações no instante `t`.
4. `renderiza.js` abre cada página no Chromium e fotografa quadro a quadro a 30 fps — o resultado não
   depende da velocidade da máquina.
5. `monta-video.py <audio> [saida.mp4]` detecta as 6 pausas entre os 7 parágrafos (ffmpeg
   `silencedetect`, do limiar mais rigoroso ao mais tolerante), usa o meio de cada pausa como troca de
   slide, renderiza e junta com a voz comprimida de leve e normalizada em duas passadas a −14 LUFS (pico ≤ −1,5 dBTP), áudio estéreo.

Sequência usada no Reel:

```
python3 transcreve.py gravacao-original.m4a palavras.json
python3 edita-audio.py gravacao-original.m4a locucao-editada.wav 7
python3 monta-video.py locucao-editada.wav reel-divida-publica.mp4
```

- `reel-divida-publica.mp4`: Reel final com a voz editada.
- `locucao-editada.m4a`: a voz depois da limpeza, sem a trilha.
- `locucao-ia.srt`: as 7 falas com os tempos do Reel, para gerar a voz por IA (TTS ou dublagem a
  partir de legenda). Números por extenso, para a voz sintética não ler símbolo. Cada bloco vai do
  início ao fim da fala na locução editada (medido com `silencedetect` a −35 dB); os cortes de slide
  caem no meio das pausas de 0,6 s entre blocos. UTF-8 sem BOM, fim de linha CRLF.

## Reel sem voz

`python3 monta-video.py --sem-audio reel-sem-audio.mp4 --fim vinheta-prisma.mp4` gera o Reel mudo com
tempo fixo de leitura por slide (`TEMPOS_SEM_AUDIO`) e a vinheta da marca no final:

| Slide | Dura (s) |
|---|---|
| Capa | 10,0 |
| Origem | 12,0 |
| Main | 11,0 |
| DRE | 12,0 |
| Cobertura | 11,0 |
| Ajuste | 15,0 |
| Aplicacao | 12,0 |
| Vinheta (fusão de 0,5 s) | 6,1 |
| **Total** | **88,6** |

Cada tempo cobre a animação (~2,5 s) e a leitura de título, número, card e legenda. O parágrafo
explicativo inteiro não cabe em tempo de Reel: quem quiser lê-lo segura o dedo na tela (o Instagram
pausa) ou lê no carrossel. O total fica abaixo de 90 s.

`vinheta-prisma.mp4` é horizontal (1280×720, 24 fps): na montagem ela é escalada pela altura, cortada
no centro (onde fica o logo), convertida para 30 fps e entra com fusão de 0,5 s de imagem e som. Os
slides levam uma faixa de áudio silenciosa; o único som é o da vinheta. A música entra depois, pela
biblioteca do Instagram.
