# -*- coding: utf-8 -*-
"""Carrossel em vídeo do post do CNPJ: um MP4 4:5 (1080x1350) por card, com as animações, recortado dos
quadros do último Reel (rode reel-cnpj.py antes). A capa ganha o "Arraste para o lado", que o Reel não tem.
Reaproveita converte.py e carrossel-videos.py do pipeline de vídeo.

Uso: python3 carrossel-cnpj.py [pasta_saida]
"""
import os, sys, json, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(os.path.dirname(AQUI), "video")
sys.path.insert(0, AQUI)

def carrega(nome, pasta, arq):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(pasta, arq))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    saida = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "carrossel-videos"))
    reel = carrega("reel_cnpj", AQUI, "reel-cnpj.py")
    plano = json.load(open(os.path.join(VIDEO, "plano-audio.json")))
    assert [p["slide"] for p in plano] == ["Cnpj" + n for n in reel.ORDEM], "rode reel-cnpj.py antes"

    # capa do carrossel: mesma página do Reel, mas com o "Arraste para o lado"
    conv = carrega("converte", VIDEO, "converte.py")
    conv.PROJ = os.path.join(AQUI, "canvas", "project")
    conv.OUT = os.path.join(VIDEO, "paginas-cnpj")
    conv.CONTADORES = {}
    conv.converte("Main", reel.NARRACAO[0], carrossel=True)
    html = open(os.path.join(conv.OUT, "Main-carrossel.html"), encoding="utf-8").read()
    for k, v in reel.BLOBS.items():
        html = html.replace("/_blob/" + k, "file://" + os.path.join(AQUI, v))
    assert "/_blob/" not in html and "Arraste" in html
    open(os.path.join(VIDEO, "paginas", "CnpjMain-carrossel.html"), "w", encoding="utf-8").write(html)

    cv = carrega("carrossel_videos", VIDEO, "carrossel-videos.py")
    sys.argv = [sys.argv[0], saida, "--vinheta", os.path.join(VIDEO, "intro-prisma.mp4")]
    cv.main()

if __name__ == "__main__":
    main()
