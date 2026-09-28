# -*- coding: utf-8 -*-
"""Reel sem voz do post do CNPJ: converte os cards em páginas 1080x1920 com legenda na tela, renderiza
quadro a quadro e acrescenta a vinheta da Prisma no final. Reaproveita converte.py e monta-video.py.

Uso: python3 reel-cnpj.py [saida.mp4]
"""
import os, sys, json, shutil, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(os.path.dirname(AQUI), "video")      # pipeline do Reel da dívida pública
sys.path.insert(0, VIDEO)

ORDEM = ["Main", "Datas", "Codigos", "ModeloII", "Norma", "Acao"]
LEGENDAS = [
    "A Receita publicou um novo modelo do comprovante do CNPJ.",
    "A data de abertura virou duas: inscrição no CNPJ e constituição.",
    "No rodapé, código QR e código de barras.",
    "O Modelo II inclui representante legal, sócios e código de autenticidade.",
    "A IN RFB nº 2.345/2026 vale desde 23/09/2026.",
    "Salve e confira o comprovante da sua empresa.",
]
# animação (~2,5 s) + leitura do card e da legenda; o card 05 cita os dois artigos na íntegra
TEMPOS = {"Main": 8.0, "Datas": 11.0, "Codigos": 8.0, "ModeloII": 11.0, "Norma": 13.0, "Acao": 10.0}
# recortes do anexo do DOU: o canvas usa /_blob/, o vídeo usa os arquivos locais
BLOBS = {"23cf6b0763d4290c886720ddec1ce63f": "anexo-modelo1.jpg", "0cb83345f6032071ecd466c0ec9278a3": "anexo-modelo2.jpg",
         "636bdaaad54e10001afb0ace169fb71a": "crop-datas.png", "7101ef130cc5bf8775e57d73d439b573": "crop-qr.png",
         "f164ad31cb9211107174cf2338f21031": "crop-qsa.png",
         "dc006f1fe22dca44823c727835b63f07": "crop-datas-2022.png"}

def carrega(nome, arq):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(VIDEO, arq))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    saida = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "reel-cnpj.mp4"))
    conv = carrega("converte", "converte.py")
    conv.PROJ = os.path.join(AQUI, "canvas", "project")
    conv.OUT = os.path.join(VIDEO, "paginas-cnpj")
    conv.CONTADORES = {}
    os.makedirs(conv.OUT, exist_ok=True)
    destino = os.path.join(VIDEO, "paginas")
    for nome, leg in zip(ORDEM, LEGENDAS):
        conv.converte(nome, leg)          # no Reel o "Arraste para o lado" sai
        html = open(os.path.join(conv.OUT, nome + ".html"), encoding="utf-8").read()
        for k, v in BLOBS.items():
            html = html.replace("/_blob/" + k, "file://" + os.path.join(AQUI, v))
        assert "/_blob/" not in html, nome
        open(os.path.join(destino, "Cnpj" + nome + ".html"), "w", encoding="utf-8").write(html)

    mv = carrega("monta_video", "monta-video.py")
    mv.ORDEM = ["Cnpj" + n for n in ORDEM]
    mv.TEMPOS_SEM_AUDIO = {"Cnpj" + k: v for k, v in TEMPOS.items()}
    mv.sem_audio(saida, os.path.join(VIDEO, "intro-prisma.mp4"))

if __name__ == "__main__":
    main()
