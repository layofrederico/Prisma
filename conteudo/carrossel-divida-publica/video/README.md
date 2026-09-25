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

`python3 monta-video.py --sem-audio reel-sem-audio.mp4` gera o Reel mudo com tempos fixos de leitura
(`TEMPOS_SEM_AUDIO`): Capa 6,0 s · Origem 7,0 s · Main 6,0 s · DRE 6,0 s · Cobertura 5,5 s ·
Ajuste 7,5 s · Aplicacao 7,0 s = 45,0 s. Leva uma faixa de áudio silenciosa para os apps aceitarem o
arquivo sem estranhar; a música entra depois, pela biblioteca do Instagram.
