# -*- coding: utf-8 -*-
"""Mixa no Reel a trilha montada a partir de 4:14 (musica414.py) e uma tecla de máquina de escrever realçada
em cada troca de card; se a trilha começa depois de 1 s, a capa abre com o solo de teclas até ela entrar.
Uso: python3 mix414.py <reel.mp4> <faixa.mp3> <musica.wav> <duracoes.json> <saida.mp4>"""
import sys, json, re, os, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
reel, faixa, musica, durs, saida = sys.argv[1:6]
info = json.load(open(musica + ".json")); durs = json.load(open(durs))
t0 = info["t0"]; trocas, acc = [], 0
for d in durs[:-1]: acc += d; trocas.append(acc)
h, m_, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([FF, "-i", reel], capture_output=True, text=True).stderr).groups()
dur = int(h) * 3600 + int(m_) * 60 + float(s)
TECLA = (16.737, 0.26)          # uma batida seca do solo de teclas (1ª tecla em 16,747 s)
ENF = "highpass=f=400,equalizer=f=4000:width_type=o:width=1.5:g=6,volume=6dB"
p = ["[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=-3dB,afade=t=in:d=0.8,"
     "afade=t=out:st=%.2f:d=0.35,adelay=%d|%d[mus]" % (info["dur"] - 0.35, int(t0 * 1000), int(t0 * 1000))]
n = len(trocas) + (1 if t0 > 1 else 0)
p.append("[2:a]asplit=%d%s" % (n, "".join("[s%d]" % i for i in range(n))))
rot = ["[mus]"]
for i, t in enumerate(trocas):
    a = max(0, int(round((t - 0.01) * 1000)))
    p.append("[s%d]atrim=start=%.3f:duration=%.2f,asetpts=PTS-STARTPTS,%s,afade=t=out:st=%.2f:d=0.08,adelay=%d|%d[k%d]"
             % (i, TECLA[0], TECLA[1], ENF, TECLA[1] - 0.08, a, a, i)); rot.append("[k%d]" % i)
if t0 > 1:   # abertura: solo de teclas até a orquestra entrar
    L = t0 + 0.6
    p.append("[s%d]atrim=start=16.737:duration=%.2f,asetpts=PTS-STARTPTS,%s,afade=t=out:st=%.2f:d=0.6[ab]"
             % (n - 1, L, ENF.replace("volume=6dB", "volume=3dB"), L - 0.6)); rot.append("[ab]")
p.append("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[v]")
p.append("%s[v]amix=inputs=%d:duration=longest:normalize=0[mix]" % ("".join(rot), len(rot) + 1))
base = ";".join(p)

def lufs(arq):
    out = subprocess.run([FF, "-hide_banner", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1])
cru, final = saida + ".cru.wav", saida + ".final.wav"
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", musica, "-i", faixa, "-filter_complex", base, "-map", "[mix]",
                "-t", "%.3f" % dur, "-c:a", "pcm_f32le", cru], check=True, capture_output=True)
ganho = -14.0 - lufs(cru)[0]
for _ in range(4):
    subprocess.run([FF, "-hide_banner", "-y", "-i", cru, "-af", "lowpass=f=15000,volume=%.2fdB,alimiter=limit=0.63:attack=1:release=80:level=false,"
                    "alimiter=limit=0.63:attack=1:release=80:level=false" % ganho, "-c:a", "pcm_f32le", final], check=True, capture_output=True)
    nivel, pico = lufs(final)
    if abs(nivel + 14) < 0.3: break
    ganho += -14.0 - nivel
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", final, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "320k", "-t", "%.3f" % dur, "-movflags", "+faststart", saida], check=True, capture_output=True)
os.remove(cru); os.remove(final)
print("ok %s | trilha entra em %.2f s | trocas %s | %.1f LUFS, pico %.1f dBFS" % (saida, t0, [round(t, 2) for t in trocas], nivel, pico))
