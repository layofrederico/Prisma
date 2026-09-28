# -*- coding: utf-8 -*-
"""Põe no Reel (sem vinheta) o trecho contínuo da faixa, sem emendas: a pancada final cai 0,5 s antes do fim.
Uso: python3 mixfinal.py <reel.mp4> <faixa.mp3> <ac.json> <saida.mp4>"""
import sys, re, os, json, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
reel, faixa, acj, saida = sys.argv[1:5]; ini = json.load(open(acj))["inicio_faixa"]
h, m_, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([FF, "-i", reel], capture_output=True, text=True).stderr).groups()
dur = int(h) * 3600 + int(m_) * 60 + float(s)
filtro = "atrim=start=%.3f:duration=%.3f,asetpts=PTS-STARTPTS,afade=t=in:d=1.0,afade=t=out:st=%.3f:d=0.45,lowpass=f=15000" % (ini, dur, dur - 0.45)
def lufs(arq):
    out = subprocess.run([FF, "-hide_banner", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1])
cru, final = saida + ".cru.wav", saida + ".final.wav"
subprocess.run([FF, "-hide_banner", "-y", "-i", faixa, "-af", filtro, "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", cru], check=True, capture_output=True)
ganho = -14.0 - lufs(cru)[0]
for _ in range(4):
    subprocess.run([FF, "-hide_banner", "-y", "-i", cru, "-af", "volume=%.2fdB,alimiter=limit=0.63:attack=1:release=80:level=false,"
                    "alimiter=limit=0.63:attack=1:release=80:level=false" % ganho, "-c:a", "pcm_f32le", final], check=True, capture_output=True)
    nivel, pico = lufs(final)
    if abs(nivel + 14) < 0.3: break
    ganho += -14.0 - nivel
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", final, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                "-t", "%.3f" % dur, "-movflags", "+faststart", saida], check=True, capture_output=True)
os.remove(cru); os.remove(final)
print("ok %s | faixa %.2f–%.2f s sem cortes | %.1f s | %.1f LUFS, pico %.1f dBFS" % (saida, ini, ini + dur, dur, nivel, pico))
