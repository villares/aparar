"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""

from __future__ import unicode_literals

import pickle
from os.path import join

import interface
from areas import Area
from pranchas import Prancha
from arquivos import lista_imagens

DEBUG = False
# offset da área que mos.tra a imagem da prancha
Prancha.ox, Prancha.oy = 200, 50
# modos (estados da ferramenta)
interface.modos = (MOVER, REMOV, CRIAR, SELEC, ZOOM) = range(5)
interface.ativo['modo'] = MOVER
# modos.ativo = MOVER  # modo indica o modo ativo
lm = len(interface.modos)
# comandos (outros comandos)
LOAD_PRANCHAS, SALVA_SESSAO, LOAD_SESSAO, GERA_CSV = range(lm, lm + 4)
PROX_PRANCHA, VOLTA_PRANCHA, PROX_PROJ, VOLTA_PROJ = range(lm + 4, lm + 8)

imagens = {}
Prancha.atual = 0
Prancha.path = sketchPath('data')

def setup():
    global img
    size(1200, 720)
    textSize(18)
    arquivo = "exemplo_prancha.jpg"  # aquivo na pasta /data/
    img = loadImage(arquivo)
    fator = float(height - 100) / img.height
    imagens["home"] = img
    p = Prancha("home")
    p.areas.append(Area(Prancha.ox, Prancha.oy,
                        img.width * fator, img.height * fator))
    Prancha.pranchas.append(p)

    interface.botoes = (  # são os textos que servem de botões na interface
        (20, 20, 140, 20, "i", "carregar (i)mgs.", LOAD_PRANCHAS),
        (20, 60, 140, 20, "s", "(s)alvar sessão", SALVA_SESSAO),
        (20, 100, 140, 20, "v", "(v)oltar sessão", LOAD_SESSAO),
        (20, 140, 140, 20, "g", "(g)erar CSV", GERA_CSV),
        # modos / estados de operaação da ferramenta
        (20, 220, 140, 20, "m", "(m)over/redim", MOVER),
        (20, 260, 140, 20, "c", "(c)riar", CRIAR),
        (20, 300, 140, 20, "r", "(r)emover", REMOV),
        (20, 340, 140, 20, "a", "(a)notar", SELEC),
        # (20, 370, 100, 40, "z", "(z)oom", ZOOM), # não implementado
        (width - 300, 20, 140, 20, RIGHT, "(→) prox. prancha", PROX_PRANCHA),
        (200, 20, 140, 20, LEFT, "(←) volta. prancha", VOLTA_PRANCHA),
    )
    # dict de funções acionadas pelos botões
    interface.comandos = {LOAD_PRANCHAS: load_pranchas,
                          SALVA_SESSAO: salva_sessao,
                          LOAD_SESSAO: load_sessao,
                          GERA_CSV: gera_csv,
                          PROX_PRANCHA: interface.prox_prancha,
                          VOLTA_PRANCHA: interface.volta_prancha,
                          }

def draw():
    global areas
    background(200)
    interface.display_botoes()  # , DEBUG=True)

    Prancha.display_nome_atual()
    Prancha.display_imagem_atual(imagens)
    Prancha.display_areas_atual(mousePressed)

def mousePressed():
    if not interface.mouse_pressed():
        areas = Prancha.get_areas_atual()
        if interface.ativo['modo'] == MOVER:
            for r in reversed(areas):
                if r.mouse_over():
                    r.drag = True
                    break
        elif interface.ativo['modo'] == REMOV:  # remover
            for r in reversed(areas[1:]):
                if r.mouse_over():
                    areas.remove(r)
                    break
        elif interface.ativo['modo'] == CRIAR:  # criar
            r = Area(mouseX, mouseY, 100, 100)
            r.drag = True
            areas.append(r)

def desselect_all():
    for r in Prancha.get_areas_atual():
        r.drag = False

def keyReleased():
    desselect_all()

def mouseReleased():
    desselect_all()
    if interface.ativo['modo'] == SELEC:
        for r in reversed(Prancha.get_areas_atual()):
            if r.mouse_over():
                r.drag = not r.drag
                break
    # else:
    #


def mouseDragged():
    for r in reversed(Prancha.get_areas_atual()):
        if r.drag:
            dx = mouseX - pmouseX
            dy = mouseY - pmouseY
            if interface.ativo['modo'] == MOVER and mouseButton == LEFT:
                x = r.x + dx
                y = r.y + dy
                na_tela = 0 < x < width - r.w and 0 < y < height - r.h
                if na_tela:
                    r.x = x
                    r.y = y
            elif interface.ativo['modo'] == MOVER and mouseButton == RIGHT:
                if r.w + dx > 2:
                    r.w = r.w + dx
                if r.h + dy > 2:
                    r.h = r.h + dy
            elif interface.ativo['modo'] == CRIAR:
                r.w = mouseX - r.x
                r.h = mouseY - r.y

def keyPressed():
    interface.key_pressed(key, keyCode)

def load_pranchas():
    selectFolder("Selecione uma pasta", "adicionar_imagens")
    # adicionar_imagens(sketchPath('data'))

def salva_sessao():
    with open(join(Prancha.path, "aparar_session.pickle"), "wb") as file:
        sessao = (Prancha.pranchas, Prancha.path)
        pickle.dump(sessao, file)
    print('Salvo em: ' + Prancha.path)


def load_sessao():
    with open(join(Prancha.path, "aparar_session.pickle"), "rb") as file:
        Prancha.pranchas, Prancha.path = pickle.load(file)
        adicionar_imagens(Prancha.path)

def gera_csv():
    pass



def adicionar_imagens(selection):
    if selection == None:
        print("Seleção cancelada.")
    else:
        dir_path = selection.getAbsolutePath()
        Prancha.path = dir_path
        print("Pasta selecionada: " + dir_path)
        for file_name, file_path in lista_imagens(dir_path):
            img = loadImage(file_path)
            img_name = file_name.split('.')[0]
            print("imagem " + img_name + " carregada.")
            imagens[img_name.lower()] = img
            fator = float(height - 100) / img.height
            if True:  # not Prancha.in_pranchas(img_name):
                p = Prancha(img_name)
                p.areas.append(Area(Prancha.ox, Prancha.oy,
                                    img.width * fator, img.height * fator))
                Prancha.pranchas.append(p)

        print len(Prancha.pranchas)
        print('Número de imagens: ' + str(len(imagens)))
