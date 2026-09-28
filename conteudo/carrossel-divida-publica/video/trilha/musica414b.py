# -*- coding: utf-8 -*-
"""Trilha a partir de 4:14, estendida sem emenda perceptível e com o final de teclas na última página.
- Emendas só em inícios de compasso (grade medida: compasso 2,276 s; 1º compasso regular em 261,373 s).
- Emenda em duas bandas: as teclas (agudos, acima de 1,8 kHz) trocam em 30 ms exatamente no tempo forte,
  então a digitação segue contínua; a orquestra (graves) funde em 1,2 s, para não se ouvir o salto.
- O último trecho da faixa (do compasso escolhido até o fim) cobre a última página do Reel, e a pancada
  final (274,881 s) cai na entrada da vinheta.
Uso: python3 musica414b.py <faixa.mp3> <pancada_no_reel_s> <inicio_ultima_pagina_s> <saida.wav>"""
import numpy as np, subprocess, json, sys, itertools, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000
INICIO, PANCADA, FIM = 254.0, 274.881, 275.25
COMP = 2.2757; ORIG = 265.925                      # grade: compassos em ORIG + k*COMP
BARRAS = [round(ORIG + k * COMP, 3) for k in range(-2, 4)]   # 261.374 ... 272.752
LACOS = {3: (265.925, 272.752), 2: (268.200, 272.752), 1: (270.476, 272.752)}   # blocos de 3, 2 e 1 compasso
M_ALTO, M_BAIXO = 0.015, 0.6                      # meia-largura das fusões (s)

def carrega(arq, filtro=None):
    cmd = [FF, "-v", "error", "-i", arq] + (["-af", filtro] if filtro else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).reshape(-1, 2).copy()

def plano(pancada, ultima):
    """Escolhe os blocos para que a música comece o mais perto possível do início do Reel (t0 >= 0)."""
    cauda_ini = min(BARRAS, key=lambda b: abs((PANCADA - b) - (pancada - ultima)))
    cab = 272.752 - INICIO; cauda = PANCADA - cauda_ini
    livre = pancada - cab - cauda; cands = []
    for x, y, z in itertools.product(range(15), range(4), range(4)):
        L = x * (LACOS[3][1] - LACOS[3][0]) + y * (LACOS[2][1] - LACOS[2][0]) + z * (LACOS[1][1] - LACOS[1][0])
        if L <= livre + 1e-6: cands.append((round(livre - L, 1), x + y + z, livre - L, x, y, z))
    _, _, *melhor = min(cands)          # menor sobra (em décimos de s) e, empatado, menos emendas
    t0, x, y, z = melhor
    segs = [(INICIO, 272.752)]
    blocos = [3] * x + [2] * y + [1] * z
    # alterna os blocos para não repetir o mesmo trecho em sequência sempre que possível
    for b in blocos: segs.append(LACOS[b])
    segs.append((cauda_ini, FIM))
    return t0, segs, cauda_ini

def monta(banda, segs, m):
    n = int(round(sum(e - s for s, e in segs) * SR)) + int(2 * m * SR) + 10
    out = np.zeros((n, 2), np.float32); pos = 0.0
    for i, (s, e) in enumerate(segs):
        ini = s - (m if i > 0 else 0); fim = e + (m if i < len(segs) - 1 else 0)
        pedaco = banda[int(round(ini * SR)):int(round(fim * SR))].copy(); L = len(pedaco); w = np.ones(L, np.float32)
        r = int(round(2 * m * SR))
        if i > 0: w[:r] = np.sin(np.linspace(0, np.pi / 2, r)) ** 2
        if i < len(segs) - 1: w[-r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
        p0 = int(round((pos - (m if i > 0 else 0)) * SR))
        out[p0:p0 + L] += pedaco * w[:, None]
        pos += e - s
    return out[:int(round(pos * SR))]

def tempos_fortes(segs, t0):
    """Inícios de compasso da grade regular, em tempo do Reel."""
    out, pos = [], t0
    for s, e in segs:
        for b in [ORIG + k * COMP for k in range(-2, 5)]:
            if s - 1e-3 <= b < e - 0.05: out.append(round(pos + b - s, 3))
        pos += e - s
    return out

if __name__ == "__main__":
    faixa, pancada, ultima, saida = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    t0, segs, cauda_ini = plano(pancada, ultima)
    cheio = carrega(faixa); grave = carrega(faixa, "lowpass=f=1800,lowpass=f=1800")
    n = min(len(cheio), len(grave)); cheio, grave = cheio[:n], grave[:n]; agudo = cheio - grave
    y = monta(grave, segs, M_BAIXO); a = monta(agudo, segs, M_ALTO); L = min(len(y), len(a)); y = y[:L] + a[:L]
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", saida],
                   input=y.astype(np.float32).tobytes(), check=True)
    fortes = tempos_fortes(segs, t0)
    ult = round(pancada - (PANCADA - cauda_ini), 3)
    json.dump({"t0": t0, "dur": L / SR, "segs": segs, "fortes": fortes, "ultima_pagina": ult}, open(saida + ".json", "w"))
    print("t0 %.2f s | blocos %s | última página começa em %.2f s (compasso %.3f da faixa) | %.2f s"
          % (t0, [round(e - s, 2) for s, e in segs], ult, cauda_ini, L / SR))
