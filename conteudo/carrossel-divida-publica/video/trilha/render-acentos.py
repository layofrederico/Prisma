# -*- coding: utf-8 -*-
"""Renderiza os Reels com as trocas nos acentos da música (ac-*.json) e sem a vinheta no final."""
import json, os, sys, importlib.util
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def carrega(nome, arq):
    s = importlib.util.spec_from_file_location(nome, arq); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
qual = sys.argv[1]; durs = json.load(open("ac-%s.json" % qual))["duracoes"]
if qual == "cnpj":
    r = carrega("reel_cnpj", os.path.join(BASE, "cnpj", "reel-cnpj.py"))
    conv = r.carrega("converte", "converte.py"); conv.PROJ = os.path.join(BASE, "cnpj", "canvas", "project")
    conv.OUT = os.path.join(r.VIDEO, "paginas-cnpj"); conv.CONTADORES = {}
    for nome, leg in zip(r.ORDEM, r.NARRACAO):
        conv.converte(nome, leg)
        html = open(os.path.join(conv.OUT, nome + ".html"), encoding="utf-8").read()
        for k, v in r.BLOBS.items(): html = html.replace("/_blob/" + k, "file://" + os.path.join(BASE, "cnpj", v))
        open(os.path.join(r.VIDEO, "paginas", "Cnpj" + nome + ".html"), "w", encoding="utf-8").write(html)
    mv = r.carrega("monta_video", "monta-video.py")
    mv.ORDEM = ["Cnpj" + n for n in r.ORDEM]; mv.TEMPOS_SEM_AUDIO = dict(zip(mv.ORDEM, durs))
else:
    mv = carrega("monta_video", os.path.join(BASE, "video", "monta-video.py"))
    mv.TEMPOS_SEM_AUDIO = dict(zip(mv.ORDEM, durs))
mv.sem_audio(os.path.abspath("reel-%s-acentos.mp4" % qual), None)
