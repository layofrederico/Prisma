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

def normaliza_voz(arq, destino, dur_total):
    """Compressão leve + loudnorm em duas passadas: -14 LUFS e pico abaixo de -1,5 dBTP.
    Em uma passada só, o loudnorm não alcança o alvo quando a voz tem pico alto e fica ~2 dB abaixo."""
    comp = destino + ".comp.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", arq, "-af",
                    "acompressor=threshold=-26dB:ratio=3:attack=5:release=90:makeup=6dB,alimiter=limit=0.7:level=false",
                    "-c:a", "pcm_s16le", comp], check=True)
    out = subprocess.run([FF, "-hide_banner", "-i", comp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
    medida = "measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % (
        m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])
    subprocess.run([FF, "-v", "error", "-y", "-i", comp, "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=11:%s,aresample=48000,apad=whole_dur=%.3f" % (medida, dur_total),
                    "-ar", "48000", destino], check=True)
    os.remove(comp)

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

    # vídeo + voz no padrão das redes (-14 LUFS), em estéreo
    voz = os.path.join(AQUI, "voz-normalizada.wav")
    normaliza_voz(audio, voz, total + SEGURA_FIM)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y",
                    "-framerate", "30", "-i", os.path.join(pasta, "%05d.jpg"),
                    "-i", voz,
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-t", "%.3f" % (total + SEGURA_FIM), "-movflags", "+faststart", saida], check=True)
    print("vídeo:", saida, "| %.1f s" % duracao(saida))

if __name__ == "__main__":
    main()
