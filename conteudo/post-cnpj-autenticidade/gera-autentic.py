# -*- coding: utf-8 -*-
"""Carrossel Prisma — código de autenticidade do comprovante do CNPJ.
Fontes: Anexo Único da IN RFB nº 2.345/2026 (DOU de 23/09/2026), art. 10 da IN RFB nº 2.119/2022 e as
páginas oficiais da Redesim em gov.br (Emitir comprovantes e Validar comprovantes).
As imagens são recortes do Modelo II publicado no DOU. Reaproveita o kit de gera-cnpj2.py."""
import os, json

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, "gera-cnpj2.py"), encoding="utf-8").read().split("\nE = 0.9")[0]
exec(_src)   # TPL2, pagina(), recorte(), rotulo(), legenda_img(), explica(), nota(), kicker(), h1(), ARRASTE ...
ROOT = os.path.join(AQUI, "autentic", "canvas")
PROJ = os.path.join(ROOT, "project")
os.makedirs(PROJ, exist_ok=True)

M2 = "/_blob/c138b2f75ea18ef3a25caec5997f4594"      # Modelo II inteiro
C_COD = "/_blob/57b0aa7f2c29d2c5547d61af3d4d397c"   # linha "Código de autenticidade"
C_QSA = "/_blob/2fd0f783488d3ddd5532c5978fbeb738"   # quadro de sócios e rodapé
C_REP = "/_blob/17abbf2712c6774cd03d793b3c3f5077"   # linha do representante legal
REF2 = "Recorte do Modelo II · Anexo Único da IN RFB nº 2.345/2026"
FONTES = "Fontes: Anexo Único da IN RFB nº 2.345/2026 (DOU de 23/09/2026); art. 10 da IN RFB nº 2.119/2022; Redesim, gov.br."

def citacao(txt, d, cor="#8ED1F5"):
    return ('''      <div class="rise" style="%s text-align: left; border-left: 6px solid %s; padding: 8px 0 8px 26px; font-size: 32px; line-height: 1.42;">%s</div>'''
            % (atraso(d), cor, txt))

# ================= 01 · Capa =================
pagina("Main.dc.html", "Código de autenticidade do CNPJ",
    kicker("COMPROVANTE DO CNPJ · MODELO II") + "\n" + h1("O que é o código de<br>autenticidade do CNPJ", 76),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 36px;">
      <div style="display: flex; flex-direction: column; align-items: center;">
%s
%s
      </div>
      <p class="rise" style="%s margin: 0; max-width: 860px; font-size: 36px; font-weight: 600; line-height: 1.35;">Um código impresso no comprovante que permite conferir, na Redesim, se o documento é autêntico.</p>
    </div>''' % (recorte(C_COD, 900, 83, "Linha Código de autenticidade do Modelo II do comprovante",
                         marcas=[(412, 4, 452, 75)]),
                 legenda_img(REF2), atraso(1.1)),
    ARRASTE)

# ================= 02 · Onde aparece =================
E2 = 400 / 1024
pagina("Onde.dc.html", "Onde o código aparece",
    kicker("ONDE ELE APARECE") + "\n" + h1("Só no Modelo II,<br>no rodapé"),
    '''    <div style="display: flex; gap: 44px; align-items: center; text-align: left;">
      <div style="display: flex; flex-direction: column; align-items: center;">
%s
%s
      </div>
      <div style="display: flex; flex-direction: column; gap: 22px; max-width: 380px;">
%s
%s
%s
      </div>
    </div>''' % (recorte(M2, 400, 561, "Modelo II do Comprovante de Inscrição e de Situação Cadastral",
                         marcas=[(int(8 * E2), int(1366 * E2), int(500 * E2), int(56 * E2))]),
                 legenda_img("Modelo II · Anexo Único"),
                 rotulo("O Anexo Único traz dois modelos: I e II", 0.9, "#8ED1F5"),
                 rotulo("O Modelo I não tem código de autenticidade", 1.15, "#8ED1F5"),
                 rotulo("No Modelo II, ele fica na última linha", 1.4)),
    explica("No modelo publicado, o código aparece como uma máscara: “Código de autenticidade: &lt;NnaNNNaNNNaaaNNN&gt;”."))

# ================= 03 · O que o Modelo II mostra =================
pagina("Conteudo.dc.html", "O que o Modelo II mostra",
    kicker("O QUE MAIS VEM NO MODELO II") + "\n" + h1("Representante<br>e sócios"),
    '''    <div style="display: flex; flex-direction: column; align-items: center; gap: 24px;">
%s
%s
%s
      <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 6px;">
%s
%s
      </div>
    </div>''' % (recorte(C_REP, 880, 64, "Linha Nome do representante legal, CPF e Qualificação do Modelo II"),
                 recorte(C_QSA, 700, 233, "Quadro de sócios e administradores e rodapé do Modelo II", d=0.5),
                 legenda_img(REF2),
                 rotulo("NOME DO REPRESENTANTE LEGAL · CPF · QUALIFICAÇÃO", 1.0, "#8ED1F5"),
                 rotulo("QUADRO DE SÓCIOS E ADMINISTRADORES", 1.25, "#8ED1F5")),
    explica("O rodapé registra quem emitiu: “Emitido no dia xx/xx/xxxx às xx:xx:xx (data e hora de Brasília) por &lt;nome do usuário logado&gt; - CPF”."))

# ================= 04 · Como conferir =================
pagina("Conferir.dc.html", "Como conferir",
    kicker("COMO CONFERIR") + "\n" + h1("Confira na Redesim"),
    '''    <div style="display: flex; flex-direction: column; gap: 34px; width: 100%%; max-width: 900px;">
%s
      <div class="rise" style="%s text-align: left; background: #FFFFFF; color: %s; border-radius: 24px; padding: 30px 34px; display: flex; flex-direction: column; gap: 12px;">
        <div style="font-size: 26px; font-weight: 700; letter-spacing: 0.08em; color: %s;">NO GOV.BR</div>
        <div style="font-size: 34px; font-weight: 700; line-height: 1.3;">Empresas e Negócios › Redesim › Validar Comprovantes › Validar Comprovante de Inscrição</div>
        <div style="font-size: 28px; line-height: 1.4; color: #3A3F7A;">“Confirme a autenticidade de Comprovante de Inscrição e Situação Cadastral no CNPJ.”</div>
      </div>
      <p class="rise" style="%s margin: 0; font-size: 28px; color: %s;">consultacnpj.redesim.gov.br/autenticidade-comprovante-inscricao</p>
    </div>''' % (citacao("No Modelo II: “O código pode ser consultado no endereço https://www.redesim.gov.br”.", 0.3, ROSA),
                 atraso(0.7), NAVY, ROSA, atraso(1.0), SOFT),
    nota(FONTES))

# ================= 05 · Quando usar =================
def passo(n, txt, d):
    return ('''      <div class="rise" style="%s display: flex; gap: 24px; align-items: center; text-align: left;">
        <span style="flex: none; width: 72px; height: 72px; border-radius: 999px; background: %s; color: %s; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center;">%d</span>
        <span style="font-size: 34px; font-weight: 600; line-height: 1.3;">%s</span>
      </div>''' % (atraso(d), WHITE, NAVY, n, txt))
pagina("Usar.dc.html", "Quando usar",
    kicker("NA PRÁTICA") + "\n" + h1("Quando vale<br>usar o Modelo II"),
    '''    <div style="display: flex; flex-direction: column; gap: 30px; width: 100%%; max-width: 880px;">
%s
%s
%s
    </div>
    <div class="rise glow" style="%s margin-top: 44px; background: %s; color: %s; border-radius: 999px; padding: 24px 48px; font-size: 38px; font-weight: 800;">Salve este post</div>''' % (
        passo(1, "Recebeu o comprovante de um fornecedor ou parceiro? Peça o que tem código de autenticidade", 0.3),
        passo(2, "Confira o código na Redesim antes de fechar contrato ou cadastrar o fornecedor", 0.6),
        passo(3, "Vai enviar o da sua empresa? Na Redesim: “Emitir Comprovante de Inscrição com Código de Autenticidade”", 0.9),
        atraso(1.3), WHITE, NAVY),
    nota("Orientação da Prisma Contábil. " + FONTES))

ORDEM = ["Main.dc.html", "Onde.dc.html", "Conteudo.dc.html", "Conferir.dc.html", "Usar.dc.html"]
TIT = ["01 · Capa", "02 · Onde aparece", "03 · O que o Modelo II mostra", "04 · Como conferir", "05 · Quando usar"]
boards = {n: {"x": (i % 3) * (1080 + 80), "y": (i // 3) * (1350 + 120), "w": 1080, "h": 1350, "title": tt}
          for i, (n, tt) in enumerate(zip(ORDEM, TIT))}
idx = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-09-28T15:10:00Z"}, "title": "Código de autenticidade do CNPJ",
       "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": ORDEM, "notes": {}, "designSystems": []}
json.dump(idx, open(os.path.join(PROJ, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok:", ", ".join(ORDEM))
