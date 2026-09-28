# -*- coding: utf-8 -*-
"""Monta a trilha a partir de 4:14 da faixa, estendida em laços de 3 compassos alinhados à grade rítmica,
com a pancada final caindo na entrada da vinheta; lista as batidas fortes para sincronizar os cortes."""
import numpy as np, subprocess, json, sys, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000
INICIO, LACO_A, LACO_B, FIM, PANCADA = 254.0, 265.925, 272.753, 275.25, 274.881   # s na faixa (grade de 105,4 bpm)
XF = int(0.012 * SR)

def carrega(arq):
    raw = subprocess.run([FF, "-v", "error", "-i", arq, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def trecho(x, a, b): return x[int(a * SR):int(b * SR)].copy()

def junta(a, b):
    r = np.linspace(0, 1, XF, dtype=np.float32)[:, None]
    return np.concatenate([a[:-XF], a[-XF:] * (1 - r) + b[:XF] * r, b[XF:]])

def monta(x, pancada_no_reel):
    cab = LACO_B - INICIO; laco = LACO_B - LACO_A; ate_pancada = PANCADA - LACO_B
    n = int((pancada_no_reel - cab - ate_pancada) // laco)
    t0 = pancada_no_reel - (cab + n * laco + ate_pancada)
    y = trecho(x, INICIO, LACO_B)
    for _ in range(n): y = junta(y, trecho(x, LACO_A, LACO_B))
    y = junta(y, trecho(x, LACO_B, FIM))
    return y, t0, n

def batidas(y, t0, limiar=5.0):
    m = y.mean(1); hp = np.diff(m, prepend=0); h = int(0.005 * SR); n = len(m) // h
    e = np.sqrt((hp[:n * h].reshape(n, h) ** 2).mean(1)); out = []
    for i in range(20, n - 20):
        loc = np.median(e[max(0, i - 100):i + 100])
        if e[i] > limiar * loc and e[i] == e[i - 10:i + 10].max(): out.append(round(t0 + i * h / SR, 3))
    return out

if __name__ == "__main__":
    faixa, pancada, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    x = carrega(faixa); y, t0, n = monta(x, pancada)
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", saida],
                   input=y.astype(np.float32).tobytes(), check=True)
    b = batidas(y, t0)
    json.dump({"t0": t0, "lacos": n, "dur": len(y) / SR, "batidas": b}, open(saida + ".json", "w"))
    print("trilha começa em %.2f s do Reel | %d laços de 3 compassos | %.2f s | %d batidas fortes" % (t0, n, len(y) / SR, len(b)))
