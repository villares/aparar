# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
from os import listdir
from os.path import isfile, join
from java.io import File
from copy import deepcopy

from pranchas import Prancha
from areas import Area
import interface

imagens = {}  # dicionário contendo as imagens carregadas

NOME_ARQ_SESSAO = "sessao_aparar_v1119b.pickle"

def lista_imagens(dir=None):
    """
    Devolve uma a lista de tuplas com os nomes dos arquivos de imagem e os caminhos
    completos para cada uma das images na pasta `dir` ou na pasta /data/ do sketch.
    Requer a função imgext() para decidir quais extensões aceitar.
    """
    data_path = dir or sketchPath('data')
    try:
        f_list = [(f, join(data_path, f)) for f in listdir(data_path)
                  if isfile(join(data_path, f)) and imgext(f)]
    except Exception as e:
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
        return []
    return f_list

def carrega_pranchas():
    # Operação normal, via callback (cuidado que silencia erros, vide opção
    # para debug!)
    selectFolder("Selecione uma pasta", "adicionar_imagens")
    # Essencial para o debug usar "chamada direta" de adicionar_imagens()
    # adicionar_imagens(File("/Users/villares/Documents/aparar/anotador_beta/data"))


def adicionar_imagens(selection):
    if selection == None:
        Prancha.avisos("seleção da pasta cancelada")
    else:
        Prancha.carregando = True
        dir_path = selection.getAbsolutePath()
        Prancha.path_sessao = dir_path
        Prancha.nome_sessao = unicode(selection)
        print("Pasta selecionada: " + dir_path)

        for file_name, file_path in lista_imagens(dir_path):
            img_name = file_name.split('.')[0]
            # imagens[img_name.lower()] = img  #file_path
            imagens[img_name.lower()] = file_path

        if not carrega_sessao() or (len(imagens) != len(Prancha.pranchas) - 1):
            for file_name, file_path in lista_imagens(dir_path):
                img = loadImage(file_path)
                img_name = file_name.split('.')[0]
                # imagens[img_name.lower()] = img  #file_path
                imagens[img_name.lower()] = file_path
                fator = Prancha.calc_fator(img)
                if not Prancha.in_pranchas(img_name):
                    p = Prancha(img_name)
                    p.areas.append(Area(interface.OX, interface.OY,
                                        img.width * fator, img.height * fator))
                    Prancha.pranchas.append(p)
            salva_sessao()

        print('Número de imagens: ' + str(len(imagens)))
        Prancha.carregando = False
        if not carrega_sessao():
            salva_sessao()

def salva_sessao():
    with open(join(Prancha.path_sessao, NOME_ARQ_SESSAO), "wb") as file:
        sessao = (Prancha.pranchas, Prancha.path_sessao, Prancha.screen_height)
        pickle.dump(sessao, file)
    mensagem = "sessão salva em …" + unicode(Prancha.path_sessao)[-40:]
    Prancha.avisos(mensagem)
    print(mensagem)

def carrega_sessao():
    from categorias import find_super_cats
    try:
        with open(join(Prancha.path_sessao, NOME_ARQ_SESSAO), "rb") as file:
            Prancha.pranchas, Prancha.path_sessao, Prancha.screen_height = pickle.load(
                file)
            # para compatibilidade com sessões antigas precisaria isto (mas zoa com tamanhos de tela diferentes)
            # Area.categorias = Prancha.pranchas[0].areas[0].categorias
            # Area.tags = Prancha.pranchas[0].areas[0].tags
            # Area.super_cats = find_super_cats(Area.categorias)
            Prancha.update_for_screen_change()
            Prancha.avisos("sessão carregada")
            return True

    except Exception as e:
        # pode ser que nãp havia
        Prancha.avisos("não foi carregada uma sessão salva")
        print "Se não imprimir 'Erro N:', pode ser bug (não é File IO) tende debug sem call-back"
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
        return False

def imgext(file_name):
    ext = file_name.split('.')[-1]
    # extensões dos formatos de imagem que o Processing aceita!
    valid_ext = ('jpg',
                 'png',
                 'jpeg',
                 'gif',
                 'tif',
                 'tga',
                 )
    return ext.lower() in valid_ext

def salva_png():
    """
    Inicialmente salva apenas imagem da "Prancha atual,
    no modo normal de edição ou modo diagrama.
    """
    diagrama = "diagrama-" if Prancha.DIAGRAMA else "imagem-"
    nome_arquivo = diagrama + Prancha.nome_prancha_atual() + ".png"
    path = join(Prancha.path_sessao, 'imagens-diagramas')
    path_arquivo = join(path, nome_arquivo)
    area = Prancha.get_areas_atual()[0]
    x, y = area.x, area.y
    w, h = int(area.w), int(area.h)
    # Para salvar só a área 100% da prancha
    # Salva img temporária da tela toda, não queria ter que usar isso :(
    temp = loadImage("temp.png")
    saveFrame(join("data", "temp.png"))
    png = createGraphics(w, h)
    png.beginDraw()
    png.background(255)
    png.copy(temp, x + 1, y + 1, w, h, 0, 0, w, h)
    png.save(path_arquivo)  # salva arquivo só com o conteúdo da área do 100%
    png.endDraw()
    if Prancha.DIAGRAMA:
        salva_legenda_diagrama(path)
    Prancha.avisos("Imagem salva: {}".format(nome_arquivo))

def salva_legenda_diagrama(path):
    png = createGraphics(300, 700)
    png.beginDraw()
    png.background(200)
    categorias = sorted(Area.categorias.keys())
    for i, cat in enumerate(categorias):
        png.fill(Area.categorias[cat]['cor'])
        png.rect(20, i * 25, 40, 20)
        png.fill(0)
        png.text(cat, 70, 15 + i * 25)
    png.save(join(path, "legenda.png"))
    png.endDraw()
