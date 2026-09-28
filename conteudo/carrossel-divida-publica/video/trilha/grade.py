# -*- coding: utf-8 -*-
"""Encaixa as trocas de card na grade rítmica da trilha: tempo forte do compasso quando estiver a até 0,8 s;
senão, a batida mais próxima; antes da parte regular da faixa, a pancada forte mais próxima (até 0,35 s)."""
import json, sys
from musica414 import INICIO, LACO_A, LACO_B, PANCADA
BAT = (LACO_B - LACO_A) / 12   # 3 compassos = 12 batidas (0,569 s)
def grade(info):
    t0, n = info["t0"], info["lacos"]; comp, bat = [], []
    for T in (263.649, 265.925, 268.201, 270.477): comp.append(t0 + T - INICIO)          # compassos da cabeça
    base = t0 + LACO_B - INICIO
    for k in range(n + 1):
        for j in range(3): comp.append(base + k * (LACO_B - LACO_A) + j * 4 * BAT)
    for c in comp:
        for j in range(4): bat.append(c + j * BAT)
    return sorted(set(round(c, 3) for c in comp)), sorted(set(round(b, 3) for b in bat))
def encaixa(limites, info):
    comp, bat = grade(info); fortes = info["batidas"]; novo = []
    for L in limites:
        c = min(comp, key=lambda v: abs(v - L)); b = min(bat, key=lambda v: abs(v - L)); f = min(fortes, key=lambda v: abs(v - L))
        if abs(c - L) <= 0.8: novo.append((c, "compasso"))
        elif abs(b - L) <= 0.3 and b > comp[0] - 0.1: novo.append((b, "batida"))
        elif abs(f - L) <= 0.35: novo.append((f, "pancada"))
        else: novo.append((L, "sem ajuste"))
    return novo
if __name__ == "__main__":
    info = json.load(open(sys.argv[1])); durs = [float(v) for v in sys.argv[2].split(",")]
    lim, acc = [], 0
    for d in durs[:-1]: acc += d; lim.append(acc)
    total = acc + durs[-1]
    novo = encaixa(lim, info); ant, out = 0, []
    for (t, tipo), L in zip(novo, lim):
        out.append(round(t - ant, 3)); print("  troca em %6.2f s -> %6.2f s (%s)" % (L, t, tipo)); ant = t
    out.append(round(total - ant, 3))
    print("  durações:", out, "| menor %.2f s | total %.2f s" % (min(out), sum(out)))
    json.dump(out, open(sys.argv[3], "w"))
