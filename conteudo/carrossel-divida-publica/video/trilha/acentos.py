# -*- coding: utf-8 -*-
"""Acha os acentos fortes do trecho contínuo da faixa (fluxo espectral) e encaixa neles as trocas de card.
A última troca fica no compasso em que começa o final de teclas; a pancada final cai 0,5 s antes do fim.
Uso: python3 acentos.py <faixa.mp3> <durações_originais> <inicio_ultima_pagina_na_faixa_s> <saida.json>"""
import sys, json, subprocess, numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 22050; PANCADA = 274.881
faixa, durs, ult_faixa, saida = sys.argv[1], [float(v) for v in sys.argv[2].split(",")], float(sys.argv[3]), sys.argv[4]
total = sum(durs); P = total - 0.5; ini = PANCADA - P
x = np.frombuffer(subprocess.run([FF, "-v", "error", "-ss", "%.3f" % ini, "-t", "%.3f" % (total + 0.5), "-i", faixa, "-ac", "1", "-ar", str(SR),
                                  "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32)
N, H = 2048, 256
w = np.hanning(N); frames = np.lib.stride_tricks.sliding_window_view(x, N)[::H] * w
S = np.log1p(np.abs(np.fft.rfft(frames, axis=1)))
flux = np.maximum(0, np.diff(S, axis=0)).sum(1); flux = np.concatenate([[0], flux])
t = np.arange(len(flux)) * H / SR
# acento = pico local (±0,25 s) bem acima da média móvel de 3 s
k = int(0.25 * SR / H); m = int(1.5 * SR / H)
acentos = []
for i in range(k, len(flux) - k):
    if flux[i] == flux[i - k:i + k + 1].max():
        loc = flux[max(0, i - m):i + m]
        z = (flux[i] - loc.mean()) / (loc.std() + 1e-9)
        if z > 1.5: acentos.append((round(float(t[i]), 3), round(float(z), 2)))
lim, acc = [], 0
for d in durs[:-1]: acc += d; lim.append(acc)
ult_reel = round(ult_faixa - ini, 3); novo = []
for j, L in enumerate(lim):
    if j == len(lim) - 1: novo.append((ult_reel, "início do final de teclas")); continue
    perto = [(a, z) for a, z in acentos if abs(a - L) <= 0.9 and a > (novo[-1][0] + 4.5 if novo else 4.5)]
    if perto:
        a, z = max(perto, key=lambda p: p[1] - 0.8 * abs(p[0] - L)); novo.append((a, "acento z=%.1f" % z))
    else: novo.append((L, "sem acento perto"))
out, ant = [], 0
for (tt, tipo), L in zip(novo, lim):
    out.append(round(tt - ant, 3)); print("  troca %6.2f -> %6.2f s (%s)" % (L, tt, tipo)); ant = tt
out.append(round(total - ant, 3))
print("  trecho da faixa: %.2f a %.2f s | pancada em %.2f s do Reel | durações %s | total %.2f" % (ini, ini + total, P, out, sum(out)))
json.dump({"duracoes": out, "inicio_faixa": ini, "acentos": acentos}, open(saida, "w"))
