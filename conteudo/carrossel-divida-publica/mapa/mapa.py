# -*- coding: utf-8 -*-
"""Contornos reais (Natural Earth 1:50m, via world-atlas) projetados para o quadro 900x400 do slide 02.
Brasil e ilhas britânicas usam escalas diferentes (ilustração, não mapa em escala), cada um com
projeção equiretangular corrigida pelo cosseno da latitude central."""
import json, math

T = json.load(open("countries-50m.json"))
SX, SY = T["transform"]["scale"]; TX, TY = T["transform"]["translate"]

def arco(i):
    rev = i < 0
    a = T["arcs"][~i if rev else i]
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * SX + TX, y * SY + TY))
    return pts[::-1] if rev else pts

def aneis(geom):
    polys = geom["arcs"] if geom["type"] == "MultiPolygon" else [geom["arcs"]]
    for poly in polys:
        for anel in poly:
            pts = []
            for i in anel:
                seg = arco(i)
                pts.extend(seg if not pts else seg[1:])
            yield pts

def dp(pts, tol):
    """Douglas-Peucker."""
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x2 * y1 - y2 * x1) / n
        if d > dmax: dmax, idx = d, k
    if dmax > tol:
        return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]

def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2

# ---- projeções
def proj_br(lon, lat):   # Brasil: 8,5 px/grau; Ponta do Seixas (-34,8) em x=230; lat -15 em y=210
    return (230 + 8.5 * math.cos(math.radians(-15)) * (lon + 34.8), 210 - 8.5 * (lat + 15))
def proj_uk(lon, lat):   # Ilhas britânicas: 20 px/grau; Londres em (820, 170)
    return (820 + 20 * math.cos(math.radians(54)) * (lon + 0.13), 170 - 20 * (lat - 51.5))

paises = {g["id"]: g for g in T["objects"]["countries"]["geometries"] if "id" in g}
def path_de(pid, proj, tol, area_min):
    partes = []
    for anel in aneis(paises[pid]):
        p = [proj(lon, lat) for lon, lat in anel]
        if area(p) < area_min: continue
        # anel fechado: simplifica as duas metades separadamente (senão o primeiro e o último ponto coincidem)
        meio = len(p) // 2
        p = dp(p[:meio + 1], tol)[:-1] + dp(p[meio:], tol)
        if len(p) < 4: continue
        partes.append("M" + " L".join("%.1f %.1f" % xy for xy in p) + " Z")
    return " ".join(partes), len(partes)

br, nbr = path_de("076", proj_br, 1.0, 20)
uk, nuk = path_de("826", proj_uk, 0.7, 6)
ie, nie = path_de("372", proj_uk, 0.7, 6)
pontos = {"rio": proj_br(-43.2, -22.9), "londres": proj_uk(-0.13, 51.5),
          "recife": proj_br(-34.9, -8.05), "lands_end": proj_uk(-5.7, 50.07), "mizen": proj_uk(-9.8, 51.45)}
json.dump({"brasil": br, "reino_unido": uk, "irlanda": ie, "pontos": pontos}, open("mapa.json", "w"), indent=1)
print("polígonos: Brasil %d | Reino Unido %d | Irlanda %d" % (nbr, nuk, nie))
print("caracteres de path: %d" % (len(br) + len(uk) + len(ie)))
for k, (x, y) in pontos.items(): print("  %-10s (%.0f, %.0f)" % (k, x, y))
