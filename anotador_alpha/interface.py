# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pranchas import Prancha
from arquivos import *
from areas import Area

# modos (estados da ferramenta)
modos = (MOVER, REMOV, CRIAR, SELEC, ZOOM) = range(5)
modo_ativo = MOVER
# comandos (outros comandos)
lm = len(modos)
LOAD_PRANCHAS, SALVA_SESSAO, LOAD_SESSAO, GERA_CSV = range(lm, lm + 4)
PROX_PRANCHA, VOLTA_PRANCHA, PROX_PROJ, VOLTA_PROJ = range(lm + 4, lm + 8)

def setup_interface():
    global botoes, comandos
    botoes = (  # são os textos que servem de botões na interface
        (20, 20, 140, 20, "i", "carregar (i)mgs.", LOAD_PRANCHAS),
        (20, 60, 140, 20, "s", "(s)alvar sessão", SALVA_SESSAO),
        (20, 100, 140, 20, "v", "(v)oltar sessão", LOAD_SESSAO),
        (20, 140, 140, 20, "g", "(g)erar CSV", GERA_CSV),
        # modos / estados de operação da ferramenta
        (20, 220, 140, 20, "m", "(m)over/redim", MOVER),
        (20, 260, 140, 20, "c", "(c)riar", CRIAR),
        (20, 300, 140, 20, "r", "(r)emover", REMOV),
        (20, 340, 140, 20, "a", "(a)notar", SELEC),
        # (20, 370, 100, 40, "z", "(z)oom", ZOOM), # não implementado
        (200, 20, 140, 20, LEFT, "(←) volta prancha", VOLTA_PRANCHA),
        (390, 20, 140, 20, RIGHT, "(→) prox. prancha", PROX_PRANCHA),
    )
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
    fator = float(height - 100) / img.height
    imagens["home"] = img
    p = Prancha("home")
    Prancha.path = sketchPath('data')
    p.areas.append(Area(Prancha.ox, Prancha.oy,
                        img.width * fator, img.height * fator))
    Prancha.pranchas.append(p)

def mouse_over(b):
    x, y, w, h, tecla, nome, const = b
    return (x < mouseX < x + w and y < mouseY < y + h)

def display_botoes(DEBUG=False):
    for b in botoes:
        x, y, w, h, tecla, nome, const = b
        if const == modo_ativo:
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
    for x, y, w, h, tecla, nome, const in botoes:
        # primeira letra do nome do botao atalho pro modo
        if tecla == k:
            if const in modos:
                modo_ativo = const
            if const in comandos:
                comandos[const]()

def mouse_pressed():
    global modo_ativo
    for b in botoes:
        x, y, w, h, tecla, nome, const = b
        if mouse_over(b):
            if const in modos:
                modo_ativo = const
            if const in comandos:
                comandos[const]()
            return
    areas = Prancha.get_areas_atual()
    if modo_ativo == MOVER:
        for r in reversed(areas):
            if r.mouse_over():
                r.selected = True
                break
    elif modo_ativo == REMOV:  # remover
        for r in reversed(areas[1:]):
            if r.mouse_over():
                areas.remove(r)
                break
    elif modo_ativo == CRIAR:  # criar
        r = Area(mouseX, mouseY, 100, 100)
        r.selected = True
        areas.append(r)

def mouse_released():
    if modo_ativo == SELEC:
        for r in reversed(Prancha.get_areas_atual()):
            if r.mouse_over():
                r.selected = not r.selected
                break

def mouse_dragged(mb):
    for r in reversed(Prancha.get_areas_atual()):
        if r.selected:
            dx = mouseX - pmouseX
            dy = mouseY - pmouseY
            if modo_ativo == MOVER and mb == LEFT:
                x = r.x + dx
                y = r.y + dy
                na_tela = 0 < x < width - r.w and 0 < y < height - r.h
                if na_tela:
                    r.x = x
                    r.y = y
            elif modo_ativo == MOVER and mb == RIGHT:
                if r.w + dx > 2:
                    r.w = r.w + dx
                if r.h + dy > 2:
                    r.h = r.h + dy
            elif modo_ativo == CRIAR:
                r.w = mouseX - r.x
                r.h = mouseY - r.y

def prox_prancha():
    Prancha.atual = (Prancha.atual + 1) % len(Prancha.pranchas)
    print(Prancha.atual)

def volta_prancha():
    Prancha.atual = (Prancha.atual - 1) % len(Prancha.pranchas)
    print(Prancha.atual)
