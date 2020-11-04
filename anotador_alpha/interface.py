# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pranchas import Prancha
from areas import Area
from categorias import setup_terms, draw_terms, select_cat, select_tag
from arquivos import imagens, carrega_pranchas, salva_sessao, carrega_sessao, gera_csv

# offset da área que mostra a imagem da prancha
OX, OY = 200, 50
rodape = 100
MIN_SIZE = 20
# menu
LOAD_PRANCHAS = "i", "carregar (i)mgs."
SALVA_SESSAO = "s", "(s)alvar sessão"
LOAD_SESSAO = "v", "(v)oltar sessão"
GERA_CSV = "g", "(g)erar CSV"

VOLTA_PRANCHA = LEFT, "(←) volta prancha"
PROX_PRANCHA = RIGHT, "(→) prox. prancha"

# modos / estados de operação da ferramenta
CRIAR = "c", "(c)riar"
EDITA = "e", "(e)editar"
REMOV = "r", "(r)emover"
ZOOM = "z", "(z)oom"  # não implementado

modos = (EDITA, REMOV, CRIAR, ZOOM)
modo_ativo = CRIAR

def setup_interface():
    Area.categorias = setup_terms("categorias.txt", 20, 300, OX - 10, 16)
    Area.tags = setup_terms("tags.txt", 20, 20 + height - rodape, width, 16)
    global botoes, comandos, categorias, tags
    botoes = {LOAD_PRANCHAS: (20, 20, 140, 20),
              SALVA_SESSAO: (20, 50, 140, 20),
              LOAD_SESSAO: (20, 80, 140, 20),
              GERA_CSV: (20, 110, 140, 20),
              # modos / estados de operação da ferramenta
              CRIAR: (20, 160, 140, 20),
              EDITA: (20, 190, 140, 20),
              REMOV: (20, 220, 140, 20),
              # ZOOM :(20, 250, 100, 40),# não implementado
              VOLTA_PRANCHA: (200, 20, 140, 20),
              PROX_PRANCHA: (390, 20, 140, 20),
              }
    # dict de funções acionadas pelos botões
    comandos = {LOAD_PRANCHAS: carrega_pranchas,
                SALVA_SESSAO: salva_sessao,
                LOAD_SESSAO: carrega_sessao,
                GERA_CSV: gera_csv,
                PROX_PRANCHA: prox_prancha,
                VOLTA_PRANCHA: volta_prancha,
                }

    splash_img_file = 'splash_img.jpg'  # aquivo na pasta /data/
    img = loadImage(splash_img_file)
    fator = Prancha.calc_fator(img)
    imagens["home"] = img
    p = Prancha("home")
    Prancha.path = sketchPath('data')
    p.areas.append(Area(OX, OY, img.width * fator, img.height * fator))
    Prancha.pranchas.append(p)


def mouse_over(b):
    x, y, w, h = botoes[b]
    return (x < mouseX < x + w and y < mouseY < y + h)

def display_botoes(DEBUG=False):
    textSize(18)
    for b in botoes:
        x, y, w, h = botoes[b]
        tecla, nome = b
        if b == modo_ativo:
            fill(200, 0, 0)
        else:
            if mouse_over(b):
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
    for b in botoes:
        x, y, w, h = botoes[b]
        tecla, nome = b
        # primeira letra do nome do botao atalho pro modo
        if tecla == k or str(tecla).upper() == k:
            if b in modos:
                modo_ativo = b
            if b in comandos:
                comandos[b]()

def mouse_pressed(mb):
    # tratamento dos botões
    global modo_ativo
    for b in botoes:
        if mouse_over(b):
            if b in modos:
                modo_ativo = b
            if b in comandos:
                comandos[b]()
            return # evita que qualquer outra ação seja realizada        
        
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
    for r in reversed(areas):
        if r.selected:
            dx = mouseX - pmouseX
            dy = mouseY - pmouseY
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
    Prancha.atual = (Prancha.atual + 1) % len(Prancha.pranchas)
    print(Prancha.atual)

def volta_prancha():
    Prancha.atual = (Prancha.atual - 1) % len(Prancha.pranchas)
    print(Prancha.atual)
