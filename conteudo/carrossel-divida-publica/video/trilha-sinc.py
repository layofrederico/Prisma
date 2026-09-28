# -*- coding: utf-8 -*-
"""Trilha com ênfase na máquina de escrever e sincronia com os cards.
- Leito: a orquestra da faixa a partir de 26 s (depois do solo de teclas), baixa, entrando aos poucos.
- Teclas: trechos do solo de máquina de escrever (16,7–25,5 s e 39,4–42,1 s), realçados em 4 kHz, cada um
  começando exatamente na entrada de um card: a primeira tecla bate no quadro em que o card aparece.
- Sai antes da vinheta, para o som dela aparecer. Vídeo copiado; áudio em -14 LUFS, pico <= -1,5 dBTP.
Uso: python3 trilha-sinc.py <reel.mp4> <trilha.mp3> <vinheta_s> <saida.mp4> <entrada_card_1> [<entrada_card_2> ...]"""
import sys, json, re, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
reel, trilha, vinheta, saida = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
cards = [float(v) for v in sys.argv[5:]]
h, m_, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([FF, "-i", reel], capture_output=True, text=True).stderr).groups()
dur = int(h) * 3600 + int(m_) * 60 + float(s)
fim_trilha = vinheta - 0.6
# (início na faixa = 10 ms antes da 1ª tecla do trecho, duração): a capa abre com o solo mais longo
RAJADAS = [(16.737, 3.0), (20.229, 1.6), (21.376, 1.6), (22.539, 1.5), (39.385, 1.7), (23.561, 1.4), (24.0, 1.6), (18.757, 1.4)]
ENF = "highpass=f=300,equalizer=f=4000:width_type=o:width=1.5:g=5,volume=4dB"

partes = ["[1:a]asplit=%d%s" % (len(cards) + 1, "".join("[t%d]" % i for i in range(len(cards) + 1)))]
partes.append("[t0]atrim=start=26:duration=%.2f,asetpts=PTS-STARTPTS,volume=-9dB,afade=t=in:d=2.5,"
              "afade=t=out:st=%.2f:d=1.2[leito]" % (dur, fim_trilha))
rotulos = ["[leito]"]
for i, t in enumerate(cards, 1):
    ini, L = RAJADAS[(i - 1) % len(RAJADAS)]
    L = min(L, max(0.4, fim_trilha - t))
    atraso = max(0, int(round((t - 0.01) * 1000)))
    partes.append("[t%d]atrim=start=%.3f:duration=%.2f,asetpts=PTS-STARTPTS,%s,afade=t=in:d=0.01,"
                  "afade=t=out:st=%.2f:d=0.3,adelay=%d|%d[k%d]" % (i, ini, L, ENF, L - 0.3, atraso, atraso, i))
    rotulos.append("[k%d]" % i)
partes.append("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[v]")
partes.append("%s[v]amix=inputs=%d:duration=longest:normalize=0,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[mix]"
              % ("".join(rotulos), len(rotulos) + 1))
base = ";".join(partes)

def lufs(arq):
    out = subprocess.run([FF, "-hide_banner", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1])

# 1) mixagem crua em WAV de 32 bits (sem cortar picos)
cru, final = saida + ".cru.wav", saida + ".final.wav"
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", trilha, "-filter_complex", base, "-map", "[mix]",
                "-t", "%.3f" % dur, "-c:a", "pcm_f32le", cru], check=True, capture_output=True)
# 2) ganho até -14 LUFS e limitador em -4 dBFS: os cliques das teclas são muito agudos e o AAC ultrapassa o pico; repete uma vez se o limitador baixar o nível
ganho = -14.0 - lufs(cru)[0]
for _ in range(4):
    subprocess.run([FF, "-hide_banner", "-y", "-i", cru, "-af", "lowpass=f=15000,volume=%.2fdB,alimiter=limit=0.63:attack=1:release=80:level=false,alimiter=limit=0.63:attack=1:release=80:level=false" % ganho,
                    "-c:a", "pcm_f32le", final], check=True, capture_output=True)
    nivel, pico = lufs(final)
    if abs(nivel + 14) < 0.3: break
    ganho += -14.0 - nivel
# 3) junta ao vídeo (copiado)
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", final, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-t", "%.3f" % dur, "-movflags", "+faststart", saida], check=True, capture_output=True)
import os; os.remove(cru); os.remove(final)
print("  mix: %.1f LUFS, pico %.1f dBFS (antes do AAC)" % (nivel, pico))
for i, t in enumerate(cards, 1):
    print("  card %d em %5.2f s  <- teclas de %.2f s da faixa" % (i, t, RAJADAS[(i - 1) % len(RAJADAS)][0] + 0.01))
print("ok", saida, "| %.1f s" % dur)
