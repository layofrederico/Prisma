# -*- coding: utf-8 -*-
"""Renderiza de novo os Reels com as durações encaixadas na grade da trilha (dur-*.json)."""
import json, os, sys, importlib.util
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def carrega(nome, arq):
    s = importlib.util.spec_from_file_location(nome, arq); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
qual = sys.argv[1]
if qual == "cnpj":
    r = carrega("reel_cnpj", os.path.join(BASE, "cnpj", "reel-cnpj.py"))
    r.TEMPOS = dict(zip(r.ORDEM, json.load(open("dur-cnpj.json"))))
    sys.argv = ["x", os.path.abspath("reel-cnpj-sinc.mp4")]; r.main()
else:
    mv = carrega("monta_video", os.path.join(BASE, "video", "monta-video.py"))
    mv.TEMPOS_SEM_AUDIO = dict(zip(mv.ORDEM, json.load(open("dur-divida.json"))))
    mv.sem_audio(os.path.abspath("reel-divida-sinc.mp4"), os.path.join(BASE, "video", "intro-prisma.mp4"))
