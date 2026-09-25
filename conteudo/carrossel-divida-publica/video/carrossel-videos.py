# -*- coding: utf-8 -*-
"""Gera o carrossel em vídeo: um MP4 4:5 (1080x1350) por slide, recortado dos quadros já renderizados
para o Reel sem voz. No carrossel, quem assiste arrasta para avançar no próprio ritmo.

Cada card toca a animação uma vez e segura o quadro final até SEGURA segundos; o Instagram repete o
vídeo em loop, e o quadro parado longo evita que os contadores recomecem enquanto a pessoa lê.

Uso (depois de `monta-video.py --sem-audio`): python3 carrossel-videos.py [pasta_saida] [--vinheta arq.mp4]
"""
import sys, os, json, subprocess
import imageio_ffmpeg

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
TOPO_SLIDE = 110   # mesmo valor de converte.py: onde o slide 4:5 começa no quadro 9:16
ANIMA = 6.0        # s — trecho animado aproveitado de cada slide (a animação mais longa leva ~4 s)
SEGURA = 30.0      # s — duração total de cada card

def main():
    args = sys.argv[1:]
    vinheta = None
    if "--vinheta" in args:
        i = args.index("--vinheta"); vinheta = args[i + 1]; del args[i:i + 2]
    saida = os.path.abspath(args[0] if args else os.path.join(AQUI, "carrossel-videos"))
    os.makedirs(saida, exist_ok=True)
    plano = json.load(open(os.path.join(AQUI, "plano-audio.json")))
    pasta = os.path.join(AQUI, "quadros-audio")
    inicio = 0
    for n, p in enumerate(plano, 1):
        quadros = round(p["dur"] * 30)
        usa = min(quadros, round(ANIMA * 30))
        arq = os.path.join(saida, "%02d-%s.mp4" % (n, p["slide"].lower()))
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y",
                        "-framerate", "30", "-start_number", str(inicio + 1), "-i", os.path.join(pasta, "%05d.jpg"),
                        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                        "-frames:v", str(round(SEGURA * 30)),
                        "-vf", "trim=end_frame=%d,crop=1080:1350:0:%d,tpad=stop_mode=clone:stop_duration=%.1f"
                               % (usa, TOPO_SLIDE, SEGURA),
                        "-map", "0:v", "-map", "1:a", "-shortest",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", arq], check=True)
        print("  card %d: %s" % (n, os.path.basename(arq)))
        inicio += quadros
    if vinheta:
        arq = os.path.join(saida, "%02d-vinheta.mp4" % (len(plano) + 1))
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.abspath(vinheta),
                        "-vf", "fps=30,scale=-2:1350:flags=lanczos,crop=1080:1350,setsar=1",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", arq],
                       check=True)
        print("  card %d: %s" % (len(plano) + 1, os.path.basename(arq)))

if __name__ == "__main__":
    main()
