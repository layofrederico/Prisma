# -*- coding: utf-8 -*-
"""Limpa a locução antes da montagem: corta o silêncio do início e do fim, encurta as pausas longas
dentro das frases e padroniza a pausa entre parágrafos (que marca a troca de slide).

Uso: python3 edita-audio.py <entrada> <saida.wav> [n_paragrafos]
Log: imprime cada pausa encontrada, a duração original e a duração final.
"""
import sys, subprocess, numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 48000
LIMIAR_DB = -45.0      # abaixo disso o quadro de 10 ms conta como silêncio
MIN_SIL = 0.08         # s — pausa mínima considerada
PAUSA_PARAGRAFO = 0.60 # s — pausa padronizada entre parágrafos (troca de slide)
PAUSA_MAX_FRASE = 0.25 # s — pausa dentro da frase acima disso é encurtada...
PAUSA_FRASE = 0.22     # s — ...para este valor
INICIO, FIM = 0.20, 0.40
FADE = int(0.012 * SR) # 12 ms de cross-fade em cada emenda, evita estalo

def carrega(arq):
    raw = subprocess.run([FF, "-v", "error", "-i", arq, "-af", "highpass=f=80", "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def silencios(x):
    h = SR // 100
    n = len(x) // h
    db = 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    mudo = db < LIMIAR_DB
    runs, i = [], 0
    while i < n:
        if mudo[i]:
            j = i
            while j < n and mudo[j]: j += 1
            if (j - i) / 100 >= MIN_SIL: runs.append((i * h, j * h))
            i = j
        else: i += 1
    return runs, n * h

def junta(a, b):
    if len(a) < FADE or len(b) < FADE: return np.concatenate([a, b])
    r = np.linspace(0, 1, FADE, dtype=np.float32)
    meio = a[-FADE:] * (1 - r) + b[:FADE] * r
    return np.concatenate([a[:-FADE], meio, b[FADE:]])

def main():
    x = carrega(sys.argv[1]); saida = sys.argv[2]
    npar = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    runs, total = silencios(x)
    # início e fim: primeiro/último trecho com voz
    ini_voz = runs[0][1] if runs and runs[0][0] == 0 else 0
    fim_voz = runs[-1][0] if runs and runs[-1][1] >= total - SR // 100 else len(x)
    internos = [r for r in runs if r[0] > ini_voz and r[1] < fim_voz]
    paragrafos = set(sorted(internos, key=lambda r: r[1] - r[0], reverse=True)[:npar - 1])
    if len(paragrafos) < npar - 1:
        raise SystemExit("Achei só %d pausas entre parágrafos (esperava %d)." % (len(paragrafos), npar - 1))

    y = x[max(0, ini_voz - int(INICIO * SR)):ini_voz]
    cursor = ini_voz
    log = []
    for a, b in internos:
        y = junta(y, x[cursor:a]) if len(y) else x[cursor:a]
        dur = (b - a) / SR
        alvo = PAUSA_PARAGRAFO if (a, b) in paragrafos else (PAUSA_FRASE if dur > PAUSA_MAX_FRASE else dur)
        alvo = min(alvo, dur)
        k = int(alvo * SR / 2)
        gap = junta(x[a:a + k], x[b - k:b]) if alvo < dur else x[a:b]
        y = junta(y, gap)
        log.append(("parágrafo" if (a, b) in paragrafos else "frase", a / SR, dur, alvo))
        cursor = b
    y = junta(y, x[cursor:fim_voz])
    y = junta(y, x[fim_voz:min(len(x), fim_voz + int(FIM * SR))])

    for tipo, t, d, alvo in log:
        marca = "" if abs(d - alvo) < 1e-3 else "  -> %.2f s" % alvo
        print("  %-9s em %6.2f s: %.2f s%s" % (tipo, t, d, marca))
    print("original: %.2f s | editado: %.2f s | cortado: %.2f s" % (len(x) / SR, len(y) / SR, (len(x) - len(y)) / SR))
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s16le", saida], input=y.astype(np.float32).tobytes(), check=True)

if __name__ == "__main__":
    main()
