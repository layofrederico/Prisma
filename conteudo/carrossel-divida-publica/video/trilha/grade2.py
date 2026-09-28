# -*- coding: utf-8 -*-
"""Encaixa as trocas de card nos tempos fortes da trilha nova; a última troca fica no início do trecho final."""
import json, sys
info = json.load(open(sys.argv[1])); durs = [float(v) for v in sys.argv[2].split(",")]
COMP = 2.2757; fortes = info["fortes"]; bat = sorted({round(f + j * COMP / 4, 3) for f in fortes for j in range(4)})
lim, acc = [], 0
for d in durs[:-1]: acc += d; lim.append(acc)
total = acc + durs[-1]; novo = []
for i, L in enumerate(lim):
    if i == len(lim) - 1: novo.append((info["ultima_pagina"], "início do final de teclas")); continue
    c = min(fortes, key=lambda v: abs(v - L)); b = min(bat, key=lambda v: abs(v - L))
    if abs(c - L) <= 0.8: novo.append((c, "tempo forte"))
    elif abs(b - L) <= 0.35: novo.append((b, "batida"))
    else: novo.append((L, "sem ajuste"))
ant, out = 0, []
for (t, tipo), L in zip(novo, lim):
    out.append(round(t - ant, 3)); print("  troca %6.2f -> %6.2f s (%s)" % (L, t, tipo)); ant = t
out.append(round(total - ant, 3)); print("  durações", out, "| total %.2f" % sum(out))
json.dump(out, open(sys.argv[3], "w"))
