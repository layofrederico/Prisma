# -*- coding: utf-8 -*-
"""Carrossel Prisma — novo comprovante do CNPJ (IN RFB nº 2.345/2026). Reaproveita o kit visual do gera7.py."""
import os, json, random

BASE = os.environ.get("PRISMA_SCRATCH", "/tmp/claude-0/-home-user-Prisma/00f81afb-b91e-5b82-b1aa-a00b4964d10b/scratchpad")
src = open(os.path.join(BASE, "gera7.py"), encoding="utf-8").read().split("\nR = 250")[0]
src = src.replace('ROOT = "%s/carrossel"' % BASE, 'ROOT = "%s/cnpj/canvas"' % BASE)
exec(src)   # NAVY, WHITE, ANIM, TPL, page(), h1(), kicker(), card(), nota(), explica(), svg(), t() ...

EXTRA = """
@keyframes popIn { from { opacity: 0; transform: scale(0.4); } to { opacity: 1; transform: scale(1); } }
@keyframes drawOnce { from { stroke-dashoffset: var(--len); } to { stroke-dashoffset: 0; } }
@keyframes glow { 0%, 100% { box-shadow: 0 0 0 0 rgba(222,58,118,0); } 50% { box-shadow: 0 0 0 10px rgba(222,58,118,0.28); } }
.pop { transform-box: fill-box; transform-origin: center; animation: popIn 0.45s cubic-bezier(0.2, 0.8, 0.3, 1.2) both; }
.draw { animation: drawOnce 1.2s ease-out both; }
.glow { animation: glow 2.4s ease-in-out infinite; }
.chegada { animation: riseIn 0.6s cubic-bezier(0.2, 0.7, 0.3, 1) both; }
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

# ---------- desenho do QR Code e do código de barras (decorativos, não codificam nada) ----------
def qr(x0, y0, mod, n=21, cor=NAVY, atraso0=0.9):
    rnd = random.Random(2345)
    partes = []
    def finder(cx, cy):
        return ('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="%d"/>'
                '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                % (x0 + cx * mod + mod // 2, y0 + cy * mod + mod // 2, 6 * mod, 6 * mod, cor, mod,
                   x0 + (cx + 2) * mod, y0 + (cy + 2) * mod, 3 * mod, 3 * mod, cor))
    reservado = lambda i, j: (i < 8 and j < 8) or (i < 8 and j > n - 9) or (i > n - 9 and j < 8)
    for i in range(n):
        for j in range(n):
            if reservado(i, j) or rnd.random() < 0.52:
                continue
            d = atraso0 + (i + j) * 0.025
            partes.append('<rect class="pop" style="%s" x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                          % (atraso(d), x0 + j * mod, y0 + i * mod, mod, mod, cor))
    partes += ['<g class="pop" style="%s">%s</g>' % (atraso(atraso0), finder(a, b)) for a, b in ((0, 0), (n - 7, 0), (0, n - 7))]
    return "\n".join(partes)

def barras(x0, y0, larg, alt, cor=NAVY):
    rnd = random.Random(23452026)
    x, out = x0, []
    while x < x0 + larg - 6:
        w = rnd.choice((2, 2, 3, 4, 6))
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y0, w, alt, cor))
        x += w + rnd.choice((2, 3, 4))
    return '<g class="grow-x" style="%s">%s</g>' % (atraso(1.6), "".join(out))

def comprovante(escala=1.0):
    """Ilustração do novo leiaute, com dados fictícios: página única, duas datas, QR Code e código de barras."""
    campo = lambda rot, val, destaque=False, d=0.5: (
        '<div class="rise" style="%s flex: 1; text-align: left; border-radius: 12px; padding: 12px 16px; %s">'
        '<div style="font-size: 18px; font-weight: 600; letter-spacing: 0.06em; color: %s;">%s</div>'
        '<div style="font-size: 27px; font-weight: 700; margin-top: 2px;">%s</div></div>'
        % (atraso(d), "background: #FDE7F0; border: 2px solid %s;" % ROSA if destaque else "background: #EEF0FA;",
           ROSA if destaque else "#4A4F8C", rot, val))
    return ('''    <div class="float" style="transform-origin: center; width: 820px; max-width: 100%%;">
    <div class="rise" style="background: #FFFFFF; color: %s; border-radius: 26px; padding: 28px 30px 24px; box-shadow: 0 24px 60px rgba(0,0,0,0.35); display: flex; flex-direction: column; gap: 14px; text-align: left;">
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px;">
        <div>
          <div style="font-size: 18px; font-weight: 600; letter-spacing: 0.14em; color: #4A4F8C;">CADASTRO NACIONAL DA PESSOA JURÍDICA</div>
          <div style="font-size: 27px; font-weight: 800; line-height: 1.15; margin-top: 4px;">Comprovante de Inscrição<br>e de Situação Cadastral</div>
        </div>
        <span class="glow" style="flex: none; background: %s; color: #FFFFFF; font-size: 20px; font-weight: 700; border-radius: 999px; padding: 8px 16px;">NOVO MODELO</span>
      </div>
      <div style="display: flex; gap: 12px;">%s</div>
      <div style="display: flex; gap: 12px;">%s%s</div>
      <div style="display: flex; gap: 18px; align-items: flex-end;">
        <div style="flex: 1; display: flex; flex-direction: column; gap: 10px;">
          <div style="height: 14px; border-radius: 7px; background: #EEF0FA; width: 92%%;"></div>
          <div style="height: 14px; border-radius: 7px; background: #EEF0FA; width: 78%%;"></div>
          <div style="height: 14px; border-radius: 7px; background: #EEF0FA; width: 85%%;"></div>
          <svg viewBox="0 0 470 70" width="470" height="70" style="max-width: 100%%; margin-top: 6px;" role="img" aria-label="Código de barras ilustrativo">%s</svg>
        </div>
        <svg viewBox="0 0 176 176" width="176" height="176" role="img" aria-label="QR Code ilustrativo" style="flex: none;">
          <rect x="0" y="0" width="176" height="176" rx="10" fill="#FFFFFF"/>
%s
        </svg>
      </div>
    </div>
    </div>
    <p style="margin: 14px 0 0; font-size: 22px; color: %s;">Ilustração com dados fictícios</p>'''
            % (NAVY, ROSA,
               campo("NÚMERO DE INSCRIÇÃO", "12.ABC.345/01DE-35", d=0.4) + campo("SITUAÇÃO CADASTRAL", "ATIVA", d=0.5),
               campo("DATA DE CONSTITUIÇÃO", "20/08/2026", True, 0.7),
               campo("DATA DE INSCRIÇÃO NO CNPJ", "25/08/2026", True, 0.85),
               barras(0, 0, 470, 70), qr(4, 4, 8), FAINT))

# ---------- ícones de traço ----------
ICONES = {
    "qr": '<rect x="6" y="6" width="16" height="16" rx="2"/><rect x="42" y="6" width="16" height="16" rx="2"/><rect x="6" y="42" width="16" height="16" rx="2"/><path d="M42 42h6v6h-6zM52 52h6v6h-6zM42 54h4M54 42v4"/>',
    "barras": '<path d="M8 10v44M16 10v44M22 10v44M30 10v44M38 10v44M44 10v44M52 10v44M58 10v44"/>',
    "datas": '<rect x="6" y="12" width="52" height="46" rx="6"/><path d="M6 26h52M20 6v12M44 6v12"/><circle cx="22" cy="42" r="4"/><circle cx="42" cy="42" r="4"/>',
    "pagina": '<path d="M16 4h24l14 14v42H16z"/><path d="M40 4v14h14M24 32h22M24 42h22M24 52h14"/>',
}
def icone(nome, cor=WHITE, tam=64):
    return ('<svg viewBox="0 0 64 64" width="%d" height="%d" fill="none" stroke="%s" stroke-width="4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (tam, tam, cor, ICONES[nome]))

def item(nome, titulo, texto, d):
    return ('''      <div class="rise" style="%s display: flex; gap: 26px; align-items: center; text-align: left; border: 2px solid %s; border-radius: 22px; padding: 16px 26px; background: rgba(255,255,255,0.04);">
        <div class="pulse" style="%s flex: none; width: 86px; height: 86px; border-radius: 22px; background: rgba(142,209,245,0.16); display: flex; align-items: center; justify-content: center;">%s</div>
        <div><div style="font-size: 36px; font-weight: 700; line-height: 1.2;">%s</div>
        <div style="font-size: 28px; line-height: 1.38; color: %s; margin-top: 4px;">%s</div></div>
      </div>''' % (atraso(d), LINE, atraso(d + 2), icone(nome), titulo, SOFT, texto))

# ================= 01 · Capa =================
pagina("Main.dc.html", "O comprovante do CNPJ mudou",
    kicker("RECEITA FEDERAL · IN RFB Nº 2.345/2026") + "\n" + h1("O comprovante do<br>CNPJ mudou", 84),
    comprovante(),
    '''    <div class="rise" style="%s display: inline-flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 600;">
      <span class="pulse" style="width: 14px; height: 14px; border-radius: 999px; background: #9FE7C4;"></span>Em vigor desde 23/09/2026</div>
%s''' % (atraso(1.2), ARRASTE))

# ================= 02 · O que mudou =================
pagina("Mudou.dc.html", "O que mudou",
    kicker("NOVO LEIAUTE") + "\n" + h1("O que mudou no<br>comprovante"),
    '''    <div style="display: flex; flex-direction: column; gap: 14px; width: 100%%; max-width: 900px;">
%s
%s
%s
%s
    </div>''' % (item("qr", "QR Code", "Espaço reservado para leitura pelo celular.", 0.3),
                 item("barras", "Código de barras", "Área própria para leitura eletrônica.", 0.5),
                 item("datas", "Duas datas", "Constituição da empresa e inscrição no CNPJ, separadas.", 0.7),
                 item("pagina", "Página única", "Leiaute reorganizado e pronto para o CNPJ com letras.", 0.9)),
    explica("A norma ainda não diz o que o QR Code vai abrir nem como será a validação. Isso depende da implantação pela Receita."))

# ================= 03 · As duas datas =================
LINHA = 440
datas_svg = svg('''      <line x1="190" y1="120" x2="%d" y2="120" stroke="%s" stroke-width="6" stroke-linecap="round"/>
      <line class="draw" style="--len: %d; stroke-dasharray: %d; animation-delay: .6s;" x1="190" y1="120" x2="%d" y2="120" stroke="%s" stroke-width="6" stroke-linecap="round"/>
      <circle class="pop" style="animation-delay: .4s;" cx="190" cy="120" r="26" fill="%s"/>
      <circle class="pop" style="animation-delay: 1.7s;" cx="%d" cy="120" r="26" fill="%s"/>
      <circle class="pulse" cx="190" cy="120" r="10" fill="%s"/>
      <circle class="pulse" style="animation-delay: .6s;" cx="%d" cy="120" r="10" fill="%s"/>
%s
%s
%s
%s''' % (190 + LINHA, TRACK, LINHA, LINHA, 190 + LINHA, GRAD and "#8ED1F5",
         ROSA, 190 + LINHA, "#8ED1F5", WHITE, 190 + LINHA, NAVY,
         t(190, 205, "Constituição", 36, weight=700, anchor="middle"),
         t(190 + LINHA, 205, "Inscrição no CNPJ", 36, weight=700, anchor="middle"),
         t(190, 250, "a empresa nasce", 28, fill=SOFT, anchor="middle"),
         t(190 + LINHA, 250, "entra no cadastro", 28, fill=SOFT, anchor="middle")), 820, 280)
pagina("Datas.dc.html", "Duas datas",
    kicker("DATA DE ABERTURA") + "\n" + h1("Onde havia uma data,<br>agora são duas"),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 26px;">
      <div class="rise" style="display: inline-flex; align-items: center; gap: 18px; font-size: 32px; font-weight: 600; color: %s;">
        <span style="text-decoration: line-through; text-decoration-color: %s; text-decoration-thickness: 4px;">Data de abertura</span>
        <span class="nudge" style="font-size: 36px;">&#8594;</span><span style="color: %s;">separada em duas</span></div>
%s
%s
    </div>''' % (SOFT, ROSA, WHITE, datas_svg,
                 card("<b>Constituição</b>: quando a empresa foi criada.<br><b>Inscrição no CNPJ</b>: quando entrou no cadastro da Receita.", 32)),
    explica("Banco, fornecedor e licitação costumam pedir o tempo de existência da empresa. Confira qual das duas datas o documento exige."))

# ================= 04 · CNPJ com letras =================
exemplo = "12.ABC.345/01DE-35"
chars = "".join('<span class="pop" style="display: inline-block; %s color: %s;">%s</span>'
                % (atraso(0.3 + i * 0.07), ROSA if ch.isalpha() else WHITE, ch) for i, ch in enumerate(exemplo))
pagina("Letras.dc.html", "CNPJ com letras",
    kicker("CNPJ ALFANUMÉRICO") + "\n" + h1("Novos CNPJs já<br>podem ter letras"),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 16px;">
      <div class="breathe" style="font-size: 82px; font-weight: 800; letter-spacing: -0.01em; font-variant-numeric: tabular-nums; white-space: nowrap;">%s</div>
      <p class="rise" style="margin: 0; font-size: 26px; color: %s; %s">Exemplo fictício · letras em rosa</p>
      <div style="display: flex; gap: 20px; margin-top: 26px; width: 100%%; max-width: 900px;">
        <div class="rise" style="%s flex: 1; border: 2px solid %s; border-radius: 22px; padding: 24px 22px;">
          <div style="font-size: 26px; color: %s;">Desde</div><div style="font-size: 46px; font-weight: 800;">31/07/2026</div>
          <div style="font-size: 26px; color: %s;">novas inscrições podem sair com letras</div></div>
        <div class="rise" style="%s flex: 1; border: 2px solid #9FE7C4; border-radius: 22px; padding: 24px 22px;">
          <div style="font-size: 26px; color: %s;">Quem já tem CNPJ</div><div style="font-size: 46px; font-weight: 800;">não muda</div>
          <div style="font-size: 26px; color: %s;">o número atual continua valendo</div></div>
      </div>
    </div>''' % (chars, FAINT, atraso(1.6), atraso(1.8), LINE, SOFT, SOFT, atraso(2.0), SOFT, SOFT),
    explica("Seu sistema, sua planilha e o cadastro de clientes e fornecedores aceitam letras no CNPJ? Vale testar antes do primeiro cliente novo."))

# ================= 05 · O que não muda =================
def ok(txt, d):
    return ('''      <div class="rise" style="%s display: flex; gap: 24px; align-items: center; text-align: left; padding: 18px 8px; border-bottom: 2px solid %s;">
        <svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true" style="flex: none;"><circle cx="32" cy="32" r="29" fill="rgba(159,231,196,0.18)" stroke="#9FE7C4" stroke-width="3"/>
          <path class="draw" style="--len: 60; stroke-dasharray: 60; %s" d="M19 33l9 9 17-19" fill="none" stroke="#9FE7C4" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span style="font-size: 38px; font-weight: 600; line-height: 1.25;">%s</span>
      </div>''' % (atraso(d), GRID, atraso(d + 0.3), txt))
pagina("NaoMuda.dc.html", "O que não muda",
    kicker("CALMA") + "\n" + h1("O que não muda"),
    '''    <div style="display: flex; flex-direction: column; width: 100%%; max-width: 880px;">
%s
%s
%s
%s
    </div>''' % (ok("Não há recadastramento", 0.3), ok("O número do CNPJ continua o mesmo", 0.6),
                 ok("Não é preciso trocar o comprovante já emitido", 0.9), ok("A norma muda o modelo do documento, não os seus dados", 1.2)),
    explica("A IN troca o modelo do comprovante (Anexo III da IN RFB nº 2.119/2022). O que está no seu cadastro continua igual."))

# ================= 06 · O que fazer =================
def passo(n, txt, d):
    return ('''      <div class="rise" style="%s display: flex; gap: 24px; align-items: center; text-align: left;">
        <span style="flex: none; width: 72px; height: 72px; border-radius: 999px; background: %s; color: %s; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center;">%d</span>
        <span style="font-size: 34px; font-weight: 600; line-height: 1.3;">%s</span>
      </div>''' % (atraso(d), WHITE, NAVY, n, txt))
pagina("Acao.dc.html", "O que fazer agora",
    kicker("CHECKLIST") + "\n" + h1("O que fazer agora"),
    '''    <div style="display: flex; flex-direction: column; gap: 30px; width: 100%%; max-width: 880px;">
%s
%s
%s
    </div>
    <div class="rise glow" style="%s margin-top: 44px; background: %s; color: %s; border-radius: 999px; padding: 24px 48px; font-size: 38px; font-weight: 800;">Comente CNPJ</div>
    <p class="rise" style="%s margin: 16px 0 0; font-size: 30px; color: %s;">e a gente confere o cadastro da sua empresa</p>''' % (
        passo(1, "Ao emitir o comprovante, confira as duas datas e os dados cadastrais", 0.3),
        passo(2, "Teste se sistemas e planilhas aceitam CNPJ com letras", 0.6),
        passo(3, "Achou erro? Corrija antes de precisar do documento", 0.9),
        atraso(1.3), WHITE, NAVY, atraso(1.5), SOFT),
    nota(FONTE + " Substitui o Anexo III da IN RFB nº 2.119/2022."))

ORDEM = ["Main.dc.html", "Mudou.dc.html", "Datas.dc.html", "Letras.dc.html", "NaoMuda.dc.html", "Acao.dc.html"]
TIT = ["01 · Capa", "02 · O que mudou", "03 · Duas datas", "04 · CNPJ com letras", "05 · O que não muda", "06 · O que fazer"]
boards = {}
for i, (n, tt) in enumerate(zip(ORDEM, TIT)):
    boards[n] = {"x": (i % 3) * (1080 + 80), "y": (i // 3) * (1350 + 120), "w": 1080, "h": 1350, "title": tt}
json.dump({"boards": boards, "order": ORDEM}, open(os.path.join(ROOT, "layout.json"), "w"), ensure_ascii=False)
print("ok:", ", ".join(ORDEM))
