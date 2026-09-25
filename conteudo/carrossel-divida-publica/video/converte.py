# -*- coding: utf-8 -*-
"""Converte os artboards .dc.html em páginas Reel 1080x1920 com controle de tempo (window.__setTime)."""
import re, os, json, sys

BASE = "/tmp/claude-0/-home-user-Prisma/00f81afb-b91e-5b82-b1aa-a00b4964d10b/scratchpad"
PROJ = BASE + "/carrossel/project"
OUT = BASE + "/video/paginas"
os.makedirs(OUT, exist_ok=True)

ORDEM = ["Capa", "Origem", "Main", "DRE", "Cobertura", "Ajuste", "Aplicacao"]
# contadores: mesmo alvo, duração e formato dos scripts dos artboards
CONTADORES = {
    "Capa":      {"valor": {"alvo": 51103.59, "dur": 1.8, "fmt": "int"}},
    "Main":      {"pib":   {"alvo": 82.5, "dur": 1.5, "fmt": "dec1"}},
    "Equacao":   {"juro":  {"alvo": 7.7, "dur": 1.5, "fmt": "dec1"},
                  "pib":   {"alvo": 1.9, "dur": 1.5, "fmt": "dec1"}},
    "Aplicacao": {"valor": {"alvo": 142465.88, "dur": 1.6, "fmt": "dec2"}},
}
TOPO_SLIDE = 110          # onde o slide 4:5 começa dentro do quadro 9:16
TOPO_LEGENDA = 1490       # faixa da legenda, abaixo do slide e acima da interface do Instagram

DRIVER = """<script>
window.__holes = %s;
function __ease(t) { return 1 - Math.pow(1 - t, 3); }
function __fmt(v, f) {
  if (f === 'int') return Math.round(v).toLocaleString('pt-BR');
  if (f === 'dec1') return v.toFixed(1).replace('.', ',');
  return v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
// posiciona TODAS as animações (CSS e contadores) no instante t, em segundos — quadro determinístico
window.__setTime = function (t) {
  document.getAnimations().forEach(function (a) { a.pause(); a.currentTime = t * 1000; });
  Object.keys(window.__holes).forEach(function (k) {
    var c = window.__holes[k], p = Math.min(1, t / c.dur), v = p >= 1 ? c.alvo : c.alvo * __ease(p);
    document.querySelectorAll('[data-hole="' + k + '"]').forEach(function (el) { el.textContent = __fmt(v, c.fmt); });
  });
};
</script>"""

def converte(nome, legenda, carrossel=False):
    s = open("%s/%s.dc.html" % (PROJ, nome), encoding="utf-8").read()
    helmet = re.search(r"<helmet>(.*?)</helmet>", s, re.S).group(1)
    helmet = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', "", helmet)
    raiz = re.search(r"</helmet>(.*)</x-dc>", s, re.S).group(1)
    raiz = re.sub(r"\{\{\s*(\w+)\s*\}\}", r'<span data-hole="\1"></span>', raiz)
    # no Reel não há o que arrastar: tira o "Arraste" da capa; o carrossel (carrossel=True) mantém
    if not carrossel:
        raiz, n = re.subn(r'<span class="arraste"[^>]*>.*?</span>\s*</span>', "", raiz, flags=re.S)
        assert n <= 1
    legenda = legenda.replace("R$ ", "R$&nbsp;")          # "R$" nunca fica sozinho no fim da linha
    assert "{{" not in raiz
    html = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="../poppins-local.css">
%s
<style>
html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #01066A; }
#slide { position: absolute; left: 0; top: %dpx; width: 1080px; height: 1350px; }
#legenda { position: absolute; left: 70px; right: 70px; top: %dpx; text-align: center;
  font-family: 'Poppins', sans-serif; font-size: 44px; font-weight: 700; line-height: 1.3; color: #FFFFFF;
  text-wrap: balance; }
</style></head>
<body>
<div id="slide">%s</div>
<div id="legenda">%s</div>
%s
</body></html>""" % (helmet, TOPO_SLIDE, TOPO_LEGENDA, raiz, legenda, DRIVER % json.dumps(CONTADORES.get(nome, {})))
    destino = "%s/%s%s.html" % (OUT, nome, "-carrossel" if carrossel else "")
    open(destino, "w", encoding="utf-8").write(html)

if __name__ == "__main__":
    legendas = json.load(open(sys.argv[1], encoding="utf-8"))
    assert len(legendas) == len(ORDEM)
    for nome, leg in zip(ORDEM, legendas):
        converte(nome, leg)
    converte("Capa", legendas[0], carrossel=True)   # capa do carrossel, com o "Arraste para o lado"
    print("convertidos:", len(ORDEM) + 1)
