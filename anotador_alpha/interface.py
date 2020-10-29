# -*- coding: utf-8 -*-
from pranchas import Prancha

botoes = []
modos = []
comandos = {}
ativo = {'modo': 0,}

def mouse_over(b):
    x, y, w, h, tecla, nome, const = b
    return (x < mouseX < x + w and y < mouseY < y + h)

def display_botoes(DEBUG=False):
    for b in botoes:
        x, y, w, h, tecla, nome, const = b
        if const == ativo['modo']:
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
    if k == CODED: k = kc
    for x, y, w, h, tecla, nome, const in botoes:
        # primeira letra do nome do botao atalho pro modo
        if tecla == k:
            if const in modos:
                ativo['modo'] = const
            if const in comandos:
                comandos[const]()

def mouse_pressed():
    for b in botoes:
        x, y, w, h, tecla, nome, const = b
        if mouse_over(b):
            if const in modos:
                ativo['modo'] = const
            if const in comandos:
                comandos[const]()
            return True
    return False


def prox_prancha():
    Prancha.atual = (Prancha.atual + 1) % len(Prancha.pranchas)
    print(Prancha.atual)

def volta_prancha():
    Prancha.atual = (Prancha.atual - 1) % len(Prancha.pranchas)
    print(Prancha.atual)
