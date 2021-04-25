# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
from os import listdir
from os.path import isfile, join, splitext
from java.io import File

from pranchas import Prancha
from areas import Area
import interface

imagens = {}  # dicionário contendo os caminhos para carregar as imagens das pranchas

NOME_ARQ_SESSAO = "sessao_aparar_v20210305.pickle"
NOME_ARQ_SESSAO_LEGADO = "sessao_aparar_v20210104ire.pickle"

def lista_imagens(dir=None):
    """
    Devolve uma a lista de tuplas com os nomes dos arquivos de imagem e os caminhos
    completos para cada uma das images na pasta `dir` ou na pasta /data/ do sketch.
    """
    def has_image_ext(file_name):
        # extensões dos formatos de imagem que o Processing aceita!
        valid_ext = ('jpg', 'png', 'jpeg', 'gif', 'tif', 'tga')
        file_ext = file_name.split('.')[-1]
        return file_ext.lower() in valid_ext

    data_path = dir or sketchPath('data')
    try:
        f_list = [(f, join(data_path, f)) for f in listdir(data_path)
                  if isfile(join(data_path, f)) and has_image_ext(f)]
    except Exception as e:
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
        return []
    return f_list

def carrega_pranchas():
    # Operação normal de adicionar_imagens() é via callback disparado por selectFolder()
    # Cuidado que o Processing silencia erros durante selectFolder, vide opção
    # para debug!
    selectFolder("Selecione uma pasta", "adicionar_imagens")
    # Para o debug, comente a linha acima e use "chamada direta" de adicionar_imagens() abaixo
    # adicionar_imagens(File("/home/villares/Área de Trabalho/APARAR/Pranchas para teste"))

def adicionar_imagens(selection):
    if selection == None:
        Prancha.avisos("seleção da pasta cancelada")
    else:
        dir_path = selection.getAbsolutePath()
        Prancha.path_sessao = dir_path
        Prancha.nome_sessao = unicode(selection)
        print("Pasta selecionada: " + dir_path)
        # ESTA PARTE FINAL MUDA NA VERSAO QUE NAO MANTEM IMAGENS NA MEMORIA
        for file_name, file_path in lista_imagens(dir_path):
            img_name = splitext(file_name)[0]
            imagens[img_name.lower()] = file_path
        if not carrega_sessao() or (len(imagens) != len(Prancha.pranchas) - 1):
            for file_name, file_path in lista_imagens(dir_path):
                Prancha.avisos("carregando imagens")
                img = loadImage(file_path)
                img_name = file_name.split('.')[0]
                imagens[img_name.lower()] = file_path
                fator = Prancha.calc_fator(img)
                if not Prancha.in_pranchas(img_name):
                    p = Prancha(img_name)
                    p.areas.append(Area(interface.OX, interface.OY,
                                        img.width * fator, img.height * fator))
                    Prancha.pranchas.append(p)

def salva_sessao():
    with open(join(Prancha.path_sessao, NOME_ARQ_SESSAO), "wb") as file:
        # Cats e tags entraram no antigo slot de Prancha.path_sessao no Pickle!
        sessao = (Prancha.pranchas, (interface.categorias, interface.tags), Prancha.screen_height)
        pickle.dump(sessao, file)
    mensagem = "sessão salva em …" + unicode(Prancha.path_sessao)[-40:]
    Prancha.avisos(mensagem)
    print(mensagem)

def carrega_sessao():
    if isfile(join(Prancha.path_sessao, NOME_ARQ_SESSAO)):
        PATH_ARQ_SESSAO = join(Prancha.path_sessao, NOME_ARQ_SESSAO)
    else:
        PATH_ARQ_SESSAO = join(Prancha.path_sessao, NOME_ARQ_SESSAO_LEGADO)        
    try:
        with open(PATH_ARQ_SESSAO, "rb") as file:
            Prancha.pranchas, cats_e_tags, Prancha.screen_height = pickle.load(file)
            Prancha.update_for_screen_change()
            Prancha.update_for_name_change()
            if cats_e_tags != Prancha.path_sessao and len(cats_e_tags) == 2: 
                # compatibilidade com arquivos antigos!
                interface.categorias, interface.tags = cats_e_tags
                print("Categorias e tags carregados da sessão salva!")
            mensagem = "Sessao carregada de …" + unicode(PATH_ARQ_SESSAO[-40:])
            Prancha.avisos(mensagem)
            print(mensagem)
            return True
    except Exception as e:
        # pode ser que não havia sessão ou outro erro...
        Prancha.avisos("não foi carregada uma sessão salva")
        print "Deve imprimir 'Erro (File IO)', senão tem algo errado!"
        print("Erro ({})".format(e))
        return False

def salva_png():
    """
    Inicialmente salva apenas imagem da "Prancha atual",
    no modo normal de edição ou modo diagrama.
    """
    modo_diagrama = interface.modo_ativo == interface.DIAGR
    prefixo = "diagrama" if modo_diagrama else "imagem"
    nome_arquivo = "{}-{}.png".format(prefixo, Prancha.nome_prancha_atual())
    sub_folder = "diagramas" if modo_diagrama else "imagens"
    path = join(Prancha.path_sessao, sub_folder)  # pasta diagramas ou imagens
    path_arquivo = join(path, nome_arquivo)
    area = Prancha.get_areas_atual()[0]
    x, y = int(area.x), int(area.y)
    w, h = int(area.w), int(area.h)
    # Para salvar só a área 100% da prancha
    # Salva img temporária da tela toda, não queria ter que usar isso :(
    saveFrame(join("data", "temp.png"))
    temp = loadImage("temp.png")
    png = createGraphics(w, h)
    png.beginDraw()
    png.background(255)
    png.copy(temp, x + 1, y + 1, w, h, 0, 0, w, h)
    png.save(path_arquivo)  # salva arquivo só com o conteúdo da área do 100%
    png.endDraw()
    if modo_diagrama:
        salva_legenda_diagrama(path)
    Prancha.avisos("Imagem salva: {}".format(nome_arquivo))

def salva_legenda_diagrama(path):
    png = createGraphics(300, 700)
    png.beginDraw()
    png.background(200)
    nomes_categorias = sorted(interface.categorias.keys())
    for i, nome_cat in enumerate(nomes_categorias):
        png.fill(Area.calc_color(nome_cat))
        png.rect(20, i * 25, 40, 20)
        png.fill(0)
        png.text(nome_cat, 70, 15 + i * 25)
    png.save(join(path, "legenda.png"))
    png.endDraw()
