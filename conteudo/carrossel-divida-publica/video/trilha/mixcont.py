# -*- coding: utf-8 -*-
"""Trilha em trecho contínuo da faixa, sem nenhuma emenda: termina com a pancada final (274,881 s) caindo
na entrada da vinheta; o início é o que couber antes disso. Sem sobreposições de teclas.
Uso: python3 mixcont.py <reel.mp4> <faixa.mp3> <vinheta_s> <saida.mp4>"""
import sys, re, os, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); PANCADA, FIM = 274.881, 275.25
reel, faixa, vinheta, saida = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
h, m_, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([FF, "-i", reel], capture_output=True, text=True).stderr).groups()
dur = int(h) * 3600 + int(m_) * 60 + float(s)
ini = PANCADA - vinheta
base = ("[1:a]atrim=start=%.3f:end=%.3f,asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "volume=-3dB,afade=t=in:d=1.0,afade=t=out:st=%.3f:d=0.3[mus];"
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[v];"
        "[mus][v]amix=inputs=2:duration=longest:normalize=0[mix]") % (ini, FIM, FIM - ini - 0.3)
def lufs(arq):
    out = subprocess.run([FF, "-hide_banner", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1])
cru, final = saida + ".cru.wav", saida + ".final.wav"
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", faixa, "-filter_complex", base, "-map", "[mix]", "-t", "%.3f" % dur,
                "-c:a", "pcm_f32le", cru], check=True, capture_output=True)
ganho = -14.0 - lufs(cru)[0]
for _ in range(4):
    subprocess.run([FF, "-hide_banner", "-y", "-i", cru, "-af", "lowpass=f=15000,volume=%.2fdB,alimiter=limit=0.63:attack=1:release=80:level=false,"
                    "alimiter=limit=0.63:attack=1:release=80:level=false" % ganho, "-c:a", "pcm_f32le", final], check=True, capture_output=True)
    nivel, pico = lufs(final)
    if abs(nivel + 14) < 0.3: break
    ganho += -14.0 - nivel
subprocess.run([FF, "-hide_banner", "-y", "-i", reel, "-i", final, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                "-t", "%.3f" % dur, "-movflags", "+faststart", saida], check=True, capture_output=True)
os.remove(cru); os.remove(final)
mm = lambda t: "%d:%04.1f" % (t // 60, t % 60)
print("ok %s | faixa de %s a %s sem cortes | 4:14 entra em %.1f s do Reel | %.1f LUFS, pico %.1f dBFS" % (saida, mm(ini), mm(FIM), 254 - ini, nivel, pico))
