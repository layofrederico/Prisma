# -*- coding: utf-8 -*-
"""Carrossel Prisma — novo comprovante do CNPJ, fiel ao texto e ao Anexo Único da IN RFB nº 2.345/2026
(DOU de 23/09/2026). As imagens dos cards são recortes do anexo publicado no DOU; nada é desenhado à mão.
Reaproveita o kit visual do gera7.py (carrossel da dívida pública)."""
import os, json

BASE = os.environ.get("PRISMA_SCRATCH", "/tmp/claude-0/-home-user-Prisma/00f81afb-b91e-5b82-b1aa-a00b4964d10b/scratchpad")
src = open(os.path.join(BASE, "gera7.py"), encoding="utf-8").read().split("\nR = 250")[0]
src = src.replace('ROOT = "%s/carrossel"' % "/tmp/claude-0/-home-user-Prisma/00f81afb-b91e-5b82-b1aa-a00b4964d10b/scratchpad",
                  'ROOT = "%s/cnpj/canvas"' % BASE)
exec(src)   # NAVY, WHITE, ANIM, TPL, h1(), kicker(), nota(), explica() ...

EXTRA = """
@keyframes popIn { from { opacity: 0; transform: scale(0.4); } to { opacity: 1; transform: scale(1); } }
@keyframes glow { 0%, 100% { box-shadow: 0 0 0 0 rgba(222,58,118,0); } 50% { box-shadow: 0 0 0 10px rgba(222,58,118,0.28); } }
.pop { transform-box: fill-box; transform-origin: center; animation: popIn 0.45s cubic-bezier(0.2, 0.8, 0.3, 1.2) both; }
.glow { animation: glow 2.4s ease-in-out infinite; }
"""
TPL2 = TPL.replace("{anim}", "{anim}" + EXTRA.replace("{", "{{").replace("}", "}}"))

def pagina(name, title, topo, centro, base):
    open(os.path.join(PROJ, name), "w", encoding="utf-8").write(
        TPL2.format(title=title, fonts=FONTS, anim=ANIM, navy=NAVY, white=WHITE,
                    grad=GRAD, topo=topo, centro=centro, base=base, script=SCRIPT_ESTATICO))

def atraso(s):
    return "animation-delay: %.2fs;" % s

ARRASTE = ('    <span class="arraste" style="display: inline-flex; align-items: center; gap: 16px; padding: 12px 30px; '
           'border-radius: 999px; border: 2px solid rgba(255,255,255,0.7); background: rgba(255,255,255,0.1); '
           'font-size: 32px; font-weight: 700; letter-spacing: 0.02em;">Arraste para o lado'
           '<span class="nudge" style="font-size: 38px; line-height: 1;">&#8594;</span></span>')
FONTE = "Fonte: IN RFB nº 2.345, de 22/09/2026 (DOU de 23/09/2026)."
REF = "Anexo Único da IN RFB nº 2.345/2026"

# recortes do anexo publicado no DOU (enviados como assets do canvas)
M1 = "/_blob/23cf6b0763d4290c886720ddec1ce63f"        # Modelo I inteiro
C_DATAS = "/_blob/636bdaaad54e10001afb0ace169fb71a"   # Modelo I, linhas 1 e 2
C_QR = "/_blob/7101ef130cc5bf8775e57d73d439b573"      # Modelo I, rodapé
C_QSA = "/_blob/f164ad31cb9211107174cf2338f21031"     # Modelo II, sócios e rodapé

def recorte(src, w, h, alt, marcas=(), d=0.3):
    """Recorte do anexo num quadro branco; marcas = retângulos (x, y, w, h) sobre o recorte exibido."""
    mk = "\n".join('      <div class="pop glow" style="%s position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; '
                   'border: 5px solid %s; border-radius: 10px;"></div>' % (atraso(d + 0.6 + k * 0.25), x, y, ww, hh, ROSA)
                   for k, (x, y, ww, hh) in enumerate(marcas))
    return ('''    <div class="rise" style="%s position: relative; background: #FFFFFF; border-radius: 18px; padding: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.35);">
      <div style="position: relative; width: %dpx; height: %dpx;">
      <img src="%s" alt="%s" style="display: block; width: %dpx; height: %dpx;">
%s
      </div>
    </div>''' % (atraso(d), w, h, src, alt, w, h, mk))

def legenda_img(txt):
    return '    <p style="margin: 12px 0 0; font-size: 24px; color: %s;">%s</p>' % (FAINT, txt)

def rotulo(txt, d, cor=ROSA):
    return ('      <div class="rise" style="%s display: flex; gap: 16px; align-items: center; text-align: left;">'
            '<span style="flex: none; width: 16px; height: 16px; border-radius: 999px; background: %s;"></span>'
            '<span style="font-size: 32px; font-weight: 700; letter-spacing: 0.02em;">%s</span></div>' % (atraso(d), cor, txt))

E = 0.9   # recortes de 1000 px de largura exibidos a 900 px

# ================= 01 · Capa: o Modelo I, como publicado =================
pagina("Main.dc.html", "Novo comprovante do CNPJ",
    kicker("IN RFB Nº 2.345, DE 22/09/2026") + "\n" + h1("Novo modelo do<br>comprovante do CNPJ", 80),
    '''    <div class="float">
%s
    </div>
%s''' % (recorte(M1, 436, 615, "Modelo I do Comprovante de Inscrição e de Situação Cadastral, Anexo Único da IN RFB nº 2.345/2026"),
         legenda_img("Modelo I · " + REF)),
    '''    <div class="rise" style="%s display: inline-flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 600;">
      <span class="pulse" style="width: 14px; height: 14px; border-radius: 999px; background: #9FE7C4;"></span>Em vigor desde a publicação no DOU, 23/09/2026</div>
%s''' % (atraso(1.2), ARRASTE))

# ================= 02 · Antes e depois das datas =================
C_2022 = "/_blob/dc006f1fe22dca44823c727835b63f07"   # Modelo I original, IN RFB nº 2.119/2022 (DOU de 08/12/2022)
def selo(txt, cor, d):
    return ('      <div class="rise" style="%s align-self: flex-start; display: inline-flex; align-items: center; gap: 12px; '
            'font-size: 26px; font-weight: 700; letter-spacing: 0.12em; color: %s;">'
            '<span style="width: 14px; height: 14px; border-radius: 999px; background: %s;"></span>%s</div>' % (atraso(d), cor, cor, txt))
K1, K2 = 860 / 942, 860 / 1000
pagina("Datas.dc.html", "Antes e depois",
    kicker("ANTES E DEPOIS") + "\n" + h1("A data de abertura<br>virou duas datas"),
    '''    <div style="display: flex; flex-direction: column; gap: 14px; width: 884px; margin-top: 18px;">
%s
%s
      <div style="height: 16px;"></div>
%s
%s
      <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 18px;">
%s
%s
      </div>
    </div>''' % (selo("ANTES · IN RFB Nº 2.119/2022", SOFT, 0.2),
                 recorte(C_2022, 860, 130, "Campo Data de abertura do Modelo I original, IN RFB nº 2.119/2022", d=0.3,
                         marcas=[(int(682 * K1), int(4 * K1), int(258 * K1), int(70 * K1))]),
                 selo("AGORA · IN RFB Nº 2.345/2026", "#9FE7C4", 0.9),
                 recorte(C_DATAS, 860, 146, "Campos Data de inscrição no CNPJ e Data de constituição do novo Modelo I", d=1.0,
                         marcas=[(int(748 * K2), int(6 * K2), int(242 * K2), int(76 * K2)),
                                 (int(748 * K2), int(100 * K2), int(242 * K2), int(60 * K2))]),
                 rotulo("DATA DE ABERTURA &#8594; DATA DE INSCRIÇÃO NO CNPJ", 1.7),
                 rotulo("NOVO CAMPO: DATA DE CONSTITUIÇÃO", 1.95)),
    explica("Recortes do Modelo I: Anexo III original da IN RFB nº 2.119/2022 e Anexo Único da IN RFB nº 2.345/2026, ambos do DOU."))

# ================= 03 · Código QR e código de barras =================
pagina("Codigos.dc.html", "Código QR e código de barras",
    kicker("NO RODAPÉ DO COMPROVANTE") + "\n" + h1("Código QR e<br>código de barras"),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 30px;">
      <div style="display: flex; flex-direction: column; align-items: center;">
%s
%s
      </div>
      <div style="display: flex; flex-direction: column; gap: 18px;">
%s
%s
      </div>
    </div>''' % (recorte(C_QR, 900, 194, "Campos Código QR e Código de barras do Modelo I",
                         marcas=[(int(8 * E), int(8 * E), int(284 * E), int(200 * E)),
                                 (int(302 * E), int(8 * E), int(690 * E), int(200 * E))]),
                 legenda_img("Recorte do Modelo I · " + REF),
                 rotulo("CÓDIGO QR", 1.2), rotulo("CÓDIGO DE BARRAS", 1.45)),
    explica("A IN traz os dois campos no modelo, mas não detalha o que cada código vai conter."))

# ================= 04 · Modelo II =================
pagina("ModeloII.dc.html", "Modelo II",
    kicker("O ANEXO TRAZ DOIS MODELOS") + "\n" + h1("O Modelo II inclui<br>sócios e autenticidade"),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 26px;">
      <div style="display: flex; flex-direction: column; align-items: center;">
%s
%s
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
%s
%s
%s
      </div>
    </div>''' % (recorte(C_QSA, 792, 264, "Quadro de sócios e administradores, código QR, código de barras e código de autenticidade do Modelo II"),
                 legenda_img("Recorte do Modelo II · " + REF),
                 rotulo("NOME DO REPRESENTANTE LEGAL · CPF · QUALIFICAÇÃO", 1.0, "#8ED1F5"),
                 rotulo("QUADRO DE SÓCIOS E ADMINISTRADORES", 1.25, "#8ED1F5"),
                 rotulo("CÓDIGO DE AUTENTICIDADE", 1.5, "#8ED1F5")),
    explica("No Modelo II: “O código pode ser consultado no endereço https://www.redesim.gov.br”."))

# ================= 05 · O que diz a IN =================
def artigo(n, txt, d, cor):
    return ('''      <div class="rise" style="%s text-align: left; border-left: 6px solid %s; padding: 6px 0 6px 28px;">
        <div style="font-size: 30px; font-weight: 800; color: %s;">%s</div>
        <div style="font-size: 33px; line-height: 1.42; margin-top: 6px;">%s</div>
      </div>''' % (atraso(d), cor, SOFT, n, txt))
pagina("Norma.dc.html", "O que diz a IN",
    kicker("TEXTO DA NORMA") + "\n" + h1("O que diz a<br>IN RFB nº 2.345/2026"),
    '''    <div style="display: flex; flex-direction: column; gap: 40px; width: 100%%; max-width: 900px;">
%s
%s
    </div>''' % (artigo("Art. 1º", "“O Anexo III da Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, denominado Comprovante de Inscrição e de Situação Cadastral, fica substituído pelo Anexo Único desta Instrução Normativa.”", 0.3, ROSA),
                 artigo("Art. 2º", "“Esta Instrução Normativa entra em vigor na data de sua publicação no Diário Oficial da União.”", 0.7, "#8ED1F5")),
    nota("Publicada no DOU de 23/09/2026. Fundamentos citados na IN: Lei nº 5.614/1970, art. 59 da LC nº 214/2025, arts. 104 e 105 do Decreto nº 12.955/2026 e Portaria MF nº 220/2026."))

# ================= 06 · O que conferir =================
def passo(n, txt, d):
    return ('''      <div class="rise" style="%s display: flex; gap: 24px; align-items: center; text-align: left;">
        <span style="flex: none; width: 72px; height: 72px; border-radius: 999px; background: %s; color: %s; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center;">%d</span>
        <span style="font-size: 34px; font-weight: 600; line-height: 1.3;">%s</span>
      </div>''' % (atraso(d), WHITE, NAVY, n, txt))
pagina("Acao.dc.html", "O que conferir",
    kicker("CHECKLIST") + "\n" + h1("O que conferir"),
    '''    <div style="display: flex; flex-direction: column; gap: 30px; width: 100%%; max-width: 880px;">
%s
%s
%s
    </div>
    <div class="rise glow" style="%s margin-top: 44px; background: %s; color: %s; border-radius: 999px; padding: 24px 48px; font-size: 38px; font-weight: 800;">Salve este post</div>
    <p class="rise" style="%s margin: 16px 0 0; font-size: 30px; color: %s;">e confira quando emitir o comprovante</p>''' % (
        passo(1, "Ao emitir o comprovante, confira a data de inscrição no CNPJ e a data de constituição", 0.3),
        passo(2, "No Modelo II, confira o representante legal e o quadro de sócios e administradores", 0.6),
        passo(3, "Encontrou divergência? Corrija antes de precisar do documento", 0.9),
        atraso(1.3), WHITE, NAVY, atraso(1.5), SOFT),
    nota(FONTE + " Substitui o Anexo III da IN RFB nº 2.119/2022."))

ORDEM = ["Main.dc.html", "Datas.dc.html", "Codigos.dc.html", "ModeloII.dc.html", "Norma.dc.html", "Acao.dc.html"]
TIT = ["01 · Capa", "02 · Duas datas", "03 · Código QR e de barras", "04 · Modelo II", "05 · O que diz a IN", "06 · O que conferir"]
for velho in ("Mudou.dc.html", "Letras.dc.html", "NaoMuda.dc.html"):
    if os.path.exists(os.path.join(PROJ, velho)):
        os.remove(os.path.join(PROJ, velho))
boards = {}
for i, (n, tt) in enumerate(zip(ORDEM, TIT)):
    boards[n] = {"x": (i % 3) * (1080 + 80), "y": (i // 3) * (1350 + 120), "w": 1080, "h": 1350, "title": tt}
json.dump({"boards": boards, "order": ORDEM}, open(os.path.join(ROOT, "layout.json"), "w"), ensure_ascii=False)
print("ok:", ", ".join(ORDEM))
