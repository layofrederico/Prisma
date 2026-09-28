# -*- coding: utf-8 -*-
"""Reel narrado do post do CNPJ: converte os cards em páginas 1080x1920 com a fala na tela, renderiza
quadro a quadro, acrescenta a vinheta da Prisma e grava o SRT da narração com os mesmos tempos.
Reaproveita converte.py e monta-video.py.

Uso: python3 reel-cnpj.py [saida.mp4]   (gera também <saida>.srt)
"""
import os, sys, math, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(os.path.dirname(AQUI), "video")      # pipeline do Reel da dívida pública
sys.path.insert(0, VIDEO)

ORDEM = ["Main", "Datas", "Codigos", "ModeloII", "Norma", "NaoExige", "Reforma", "Acao"]
# a fala de cada card: vira legenda na tela e bloco do SRT
NARRACAO = [
    "A Receita Federal publicou um novo modelo do comprovante do CNPJ.",
    "No lugar da data de abertura, agora aparecem duas datas: a de inscrição no CNPJ e a de constituição.",
    "No rodapé, entram código QR e código de barras. A norma ainda não detalha o que eles vão conter.",
    "O Modelo II traz também representante legal, quadro de sócios e código de autenticidade.",
    "A Instrução Normativa 2.345 tem só dois artigos e vale desde 23 de setembro de 2026.",
    "Ela só troca o modelo. Não cria recadastramento, prazo, taxa nem obrigação nova.",
    "E cita o cadastro único da reforma tributária: CPF, CNPJ e CIB.",
    "Na próxima emissão, confira as duas datas e os dados da sua empresa. Salve este post.",
]
PALAVRAS_POR_S = 2.5   # ritmo de locução em português (150 palavras por minuto)
ENTRADA = 0.4          # s — a fala começa logo depois de o card entrar
FOLGA = 1.0            # s — respiro depois da fala, antes do próximo card
MINIMO = 5.0           # s — a animação mais longa do card leva ~2,5 s

def fala(txt):
    return len(txt.split()) / PALAVRAS_POR_S

TEMPOS = {n: max(MINIMO, math.ceil((ENTRADA + fala(t) + FOLGA) * 10) / 10) for n, t in zip(ORDEM, NARRACAO)}

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

def tc(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

def grava_srt(caminho):
    linhas, t0 = [], 0.0
    for i, (n, txt) in enumerate(zip(ORDEM, NARRACAO), 1):
        ini, fim = t0 + ENTRADA, t0 + ENTRADA + fala(txt)
        linhas += [str(i), "%s --> %s" % (tc(ini), tc(fim)), txt, ""]
        print("  %02d %-9s card %5.1f–%5.1f s | fala %5.1f–%5.1f s | %2d palavras"
              % (i, n, t0, t0 + TEMPOS[n], ini, fim, len(txt.split())))
        t0 += TEMPOS[n]
    open(caminho, "w", encoding="utf-8", newline="\r\n").write("\n".join(linhas))

def main():
    saida = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "reel-cnpj.mp4"))
    grava_srt(os.path.splitext(saida)[0] + ".srt")
    conv = carrega("converte", "converte.py")
    conv.PROJ = os.path.join(AQUI, "canvas", "project")
    conv.OUT = os.path.join(VIDEO, "paginas-cnpj")
    conv.CONTADORES = {}
    os.makedirs(conv.OUT, exist_ok=True)
    destino = os.path.join(VIDEO, "paginas")
    for nome, leg in zip(ORDEM, NARRACAO):
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
