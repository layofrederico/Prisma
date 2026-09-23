# Montagem do vídeo com a voz gravada

1. `converte.py` transforma cada slide `.dc.html` numa página 1080×1920 (slide 4:5 no alto, legenda
   embaixo) com `window.__setTime(t)`, que posiciona todas as animações no instante `t`.
2. `renderiza.js` abre cada página no Chromium e fotografa quadro a quadro a 30 fps — o resultado não
   depende da velocidade da máquina.
3. `monta-video.py <audio>` detecta as 9 pausas entre os 10 parágrafos (ffmpeg `silencedetect`, do
   limiar mais rigoroso ao mais tolerante), usa o meio de cada pausa como troca de slide, renderiza e
   junta com a voz normalizada a −14 LUFS.

`previa-reel-sem-audio.mp4`: prévia com os tempos do roteiro, sem áudio.
