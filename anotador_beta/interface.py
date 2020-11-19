# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pranchas import Prancha
from areas import Area
from categorias import setup_terms, draw_terms, select_cat, select_tag, find_super_cats
from arquivos import imagens, carrega_pranchas, salva_sessao, carrega_sessao, gera_csv, salva_png

# offset da área que mostra a imagem da prancha
OX, OY = 200, 50
rodape = 50
MIN_SIZE = 20
# menu
LOAD_PRANCHAS = "i", "carregar [i]magens"
SALVA_SESSAO = "s", "[s]alvar sessão"
LOAD_SESSAO = "c", "[c]arregar sessão"
GERA_CSV = "g", "[g]erar CSV"
SALVA_PNG = "p", "salvar [p]ng"
DIAGR = "d", "mostra [d]iagrama"

VOLTA_PRANCHA = LEFT, "[←] volta prancha"
PROX_PRANCHA = RIGHT, "[→] prox. prancha"
ROT_PRANCHA = "9", "girar [p]rancha 90°"

# modos / estados de operação da ferramenta
CRIAR = "a", "[a]dicionar áreas"
EDITA = "e", "[e]ditar áreas"
ED100 = "t", "edi[t]ar 100%"
REMOV = "r", "[r]emover áreas" # desabilitado
ZOOM = "z", "[z]oom"  # não implementado

modos = (EDITA, ED100, REMOV, CRIAR, ZOOM, DIAGR)
modo_ativo = CRIAR
Prancha.DIAGRAMA = False

def setup_interface():
    cf, tf = "categorias.txt", "tags.txt"
    Prancha.path_sessao = Prancha.path_sessao or sketchPath('data')
    Prancha.screen_height = height - (OY + rodape)

    Area.categorias = setup_terms(cf, 20, 380, OX - 10, 16)
    Area.super_cats = find_super_cats(Area.categorias)
    Area.tags = setup_terms(
        tf, 20 + OX, 4 + height - rodape, width - 20, 14, wgap=10)
    global botoes, comandos, categorias, tags
    botoes = {
        ("", "ARQUIVOS"): (20, 20, 140, 20),
        LOAD_PRANCHAS: (20, 50, 140, 20),
        SALVA_SESSAO: (20, 80, 140, 20),
        # LOAD_SESSAO: (20, 110, 140, 20),
        GERA_CSV: (20, 140, 140, 20),
        SALVA_PNG: (20, 170, 140, 20),
        # modos / estados de operação da ferramenta
        ("", "ÁREAS"): (20, 240, 140, 20),
        CRIAR: (20, 270, 140, 20),
        EDITA: (20, 300, 140, 20),
        ED100: (20, 330, 140, 20),
        DIAGR: (20, 360, 140, 20),
        # REMOV: (20, 360, 140, 20),
        # ZOOM :(20, 390, 100, 40),# não implementado
        VOLTA_PRANCHA: (200, 20, 140, 20),
        PROX_PRANCHA: (390, 20, 140, 20),
        ROT_PRANCHA: (580, 20, 140, 20),
    }
    # dict de funções acionadas pelos botões
    comandos = {LOAD_PRANCHAS: carrega_pranchas,
                SALVA_SESSAO: salva_sessao,
                LOAD_SESSAO: carrega_sessao,
                GERA_CSV: gera_csv,
                PROX_PRANCHA: prox_prancha,
                VOLTA_PRANCHA: volta_prancha,
                ROT_PRANCHA: rot_prancha,
                SALVA_PNG: salva_png,
                DIAGR: diagrama_on,
                }

    splash_img_file = 'splash_img.jpg'  # aquivo na pasta /data/
    img = loadImage(splash_img_file)
    fator = Prancha.calc_fator(img)
    imagens["000"] = img
    p = Prancha("000")
    Prancha.path = sketchPath('data')
    p.areas.append(Area(OX, OY, img.width * fator, img.height * fator))
    Prancha.pranchas.append(p)

def diagrama_on():
    Prancha.DIAGRAMA = True

def mouse_over(b):
    x, y, w, h = botoes[b]
    return (x < mouseX < x + w and y < mouseY < y + h)

def display_botoes(DEBUG=False):
    textSize(18)
    for b in botoes:
        x, y, w, h = botoes[b]
        tecla, nome = b
        if b == modo_ativo:
            fill(0, 0, 200)
        else:
            if mouse_over(b) and tecla != "":
                fill(255)
            else:
                fill(0)
        if DEBUG:
            push()
            noFill()
            rect(x, y, w, h)  # área clicável do texto dos botoes
            pop()
        # textAlign(LEFT, CENTER)
        text(nome, x, y + h / 2)

def key_pressed(k, kc):
    global modo_ativo
    if k == CODED:
        k = kc

    if k == DELETE or k == BACKSPACE:
       areas = Prancha.get_areas_atual()
       for a in areas[1:]:
         if a.selected:
            areas.remove(a) 
            break

    for b in botoes:
        x, y, w, h = botoes[b]
        tecla, nome = b
        # primeira letra do nome do botao atalho pro modo
        if tecla == k or str(tecla).upper() == k:
            if b in modos:
                modo_ativo = b
                if modo_ativo != DIAGR:
                    Prancha.DIAGRAMA = False
            if b in comandos:
                comandos[b]()

def mouse_pressed(mb):
    # tratamento dos botões
    global modo_ativo
    for b in botoes:
        if mouse_over(b):
            if b in modos:
                modo_ativo = b
                if modo_ativo != DIAGR:
                    Prancha.DIAGRAMA = False
            if b in comandos:
                comandos[b]()
            return  # evita que qualquer outra ação seja realizada

    areas = Prancha.get_areas_atual()
    # tratamento dos tags e categorias
    if modo_ativo in (EDITA, CRIAR):
        for a in areas:
            if a.selected:
                a.cat_and_tag_selection()
    # tratamento dos objetos Area
    if modo_ativo == EDITA:  # editar
        for a in reversed(areas):
            if a.mouse_over():
                Prancha.desselect_all()
                a.selected = True
                break
    elif modo_ativo == REMOV:  # remover
        for a in reversed(areas[1:]):
            if a.mouse_over():
                areas.remove(a)
                break
    elif modo_ativo == CRIAR and mb == LEFT:  # criar
        if areas[0].mouse_over():
            Prancha.desselect_all()
            a = Area(mouseX, mouseY, MIN_SIZE, MIN_SIZE)
            a.selected = True
            areas.append(a)

def mouse_dragged(mb):
    areas = Prancha.get_areas_atual()
    dx, dy = mouseX - pmouseX, mouseY - pmouseY
    a0 = areas[0]
    if modo_ativo == ED100:
        if mb == LEFT:
            x = a0.x + dx
            y = a0.y + dy
            na_tela = 0 < x < width - a0.w and 0 < y < height - a0.h
            if na_tela:
                a0.x = x
                a0.y = y
        else:
            if a0.w + dx > MIN_SIZE:
                a0.w += dx
            if a0.h + dy > MIN_SIZE:
                a0.h += dy
    for r in reversed(areas[1:]):
        if r.selected:
            if modo_ativo == EDITA and mb == LEFT:
                x = r.x + dx
                y = r.y + dy
                na_tela = 0 < x < width - r.w and 0 < y < height - r.h
                if na_tela:
                    r.x = x
                    r.y = y
            elif modo_ativo in (EDITA, CRIAR) and mb == RIGHT:
                if r.w + dx > MIN_SIZE:
                    r.w = r.w + dx
                if r.h + dy > MIN_SIZE:
                    r.h = r.h + dy
            elif modo_ativo == CRIAR and areas[0].mouse_over():
                if mouseX - r.x > MIN_SIZE:
                    r.w = mouseX - r.x
                if mouseY - r.y > MIN_SIZE:
                    r.h = mouseY - r.y

def prox_prancha():
    Prancha.i_atual = (Prancha.i_atual + 1) % len(Prancha.pranchas)

def volta_prancha():
    Prancha.i_atual = (Prancha.i_atual - 1) % len(Prancha.pranchas)

def rot_prancha():
    pa = Prancha.pranchas[Prancha.i_atual]
    pa.rot = (pa.rot + 1) % 4
    img, rot, fator = Prancha.imagem_rot_fator_atual(imagens)
    if img and (rot == 1 or rot == 3):
        pa.areas[0] = Area(
            OX, OY, img.height * fator, img.width * fator)  # INVERTED
    elif img:
        pa.areas[0] = Area(OX, OY, img.width * fator, img.height * fator)
        
def yes_no_pane(title, message):
    # Sim é 0, Não é 1, fechar a janela é -1
    from javax.swing import JOptionPane
    return JOptionPane.showConfirmDialog(None,
                                         message,
                                         title,
                                         JOptionPane.YES_NO_OPTION)
