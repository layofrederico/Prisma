# Trilha a partir de 4:14, sincronizada com os cards

Scripts que põem a trilha nos Reels sem voz (CNPJ e dívida pública). A faixa MP3 não está versionada.

1. `musica414.py <faixa.mp3> <pancada_s> <saida.wav>` monta a trilha:
   - começa em **4:14 (254,0 s)** da faixa, no trecho em que a orquestra cresce com a máquina de escrever;
   - estende a música repetindo 3 compassos de **265,925 s a 272,753 s**, cortados na grade rítmica medida
     na própria faixa (semicolcheia de 0,1423 s, 105,4 bpm), com emenda de 12 ms;
   - faz a **pancada final (274,88 s)** cair exatamente na entrada da vinheta.
2. `grade.py <musica.wav.json> <durações> <saida.json>` move cada troca de card para o tempo forte do
   compasso mais próximo (até 0,8 s de distância), senão para a batida mais próxima (até 0,3 s).
3. `render-sinc.py cnpj|divida` renderiza os Reels de novo com essas durações.
4. `mix414.py` mixa a trilha (−3 dB), uma tecla realçada em cada troca de card e, no Reel do CNPJ, o solo
   de teclas na abertura até a orquestra entrar. Volume final em −14 LUFS, pico −3 dBFS.

| Reel | A trilha entra em | Repetições dos 3 compassos | Trocas de card (s) |
|---|---|---|---|
| CNPJ (64,9 s) | 3,78 s | 5 | 5,90 · 15,13 · 23,67 · 31,64 · 38,46 · 45,29 · 52,12 |
| Dívida (88,6 s) | 0,17 s | 9 | 9,82 · 21,77 · 32,58 · 45,09 · 55,34 · 71,27 |

A faixa é "With My Own Eyes" (Dario Marianelli, *Atonement*, 2007), obra protegida: ver o alerta de
direitos autorais antes de publicar.
