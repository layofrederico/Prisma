# -*- coding: utf-8 -*-
"""Integra o áudio gravado ao carrossel: detecta as pausas entre parágrafos, casa um trecho por slide,
renderiza cada slide com a duração do seu trecho e gera o Reel 1080x1920 com a voz.

Uso: python3 monta-video.py <audio> [saida.mp4]
"""
import sys, os, re, json, subprocess, shutil
import imageio_ffmpeg

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
ORDEM = ["Capa", "Origem", "Main", "DRE", "Cobertura", "Ajuste", "Aplicacao"]
MIN_SLIDE = 2.6       # s — tempo para as animações terminarem (a mais longa leva ~2,4 s)
SEGURA_FIM = 1.5      # s — o último slide fica parado depois da última palavra

def duracao(arq):
    out = subprocess.run([FF, "-hide_banner", "-i", arq], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

def silencios(arq, ruido_db, minimo):
    out = subprocess.run([FF, "-hide_banner", "-i", arq, "-af", "silencedetect=noise=%ddB:d=%s" % (ruido_db, minimo),
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(ini, fim))

def cortes(arq):
    total = duracao(arq)
    # tenta limiares do mais rigoroso ao mais tolerante até achar as pausas entre os parágrafos
    for ruido in (-40, -35, -30, -25):
        sil = silencios(arq, ruido, 0.35)
        internos = [(a, b) for a, b in sil if a > 0.3 and b < total - 0.3]   # descarta silêncio de início e de fim
        if len(internos) >= len(ORDEM) - 1:
            maiores = sorted(sorted(internos, key=lambda p: p[1] - p[0], reverse=True)[:len(ORDEM) - 1])
            return total, [(a + b) / 2 for a, b in maiores], ruido
    raise SystemExit("Encontrei só %d pausas entre parágrafos (preciso de %d). Regrave com uma pausa de "
                     "1 segundo entre cada parágrafo, ou me passe os tempos de troca de slide." % (len(internos), len(ORDEM) - 1))

def main():
    audio = os.path.abspath(sys.argv[1])
    saida = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQUI, "reel-com-audio.mp4"))
    total, pontos, ruido = cortes(audio)
    limites = [0.0] + pontos + [total + SEGURA_FIM]
    plano = [{"slide": s, "dur": round(limites[i + 1] - limites[i], 3)} for i, s in enumerate(ORDEM)]

    print("áudio: %.1f s | limiar de silêncio: %d dB" % (total, ruido))
    for i, p in enumerate(plano, 1):
        aviso = "  <- curto: a animação pode não terminar" if p["dur"] < MIN_SLIDE else ""
        print("  %02d %-14s entra em %5.1f s | dura %4.1f s%s" % (i, p["slide"], limites[i - 1], p["dur"], aviso))

    json.dump(plano, open(os.path.join(AQUI, "plano-audio.json"), "w"), indent=1)
    pasta = os.path.join(AQUI, "quadros-audio")
    shutil.rmtree(pasta, ignore_errors=True)
    env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
    subprocess.run(["node", os.path.join(AQUI, "renderiza.js"), os.path.join(AQUI, "plano-audio.json"), pasta, "30"],
                   check=True, env=env)

    # vídeo + voz; loudnorm deixa o volume no padrão das redes (-14 LUFS)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y",
                    "-framerate", "30", "-i", os.path.join(pasta, "%05d.jpg"),
                    "-i", audio,
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,apad",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", saida], check=True)
    print("vídeo:", saida, "| %.1f s" % duracao(saida))

if __name__ == "__main__":
    main()
