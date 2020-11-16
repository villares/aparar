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
    # Operação normal, via callback (que silencia erros!)
    selectFolder("Selecione uma pasta", "adicionar_imagens")
    # Essencial para o debug usar "chamada direta" de adicionar_imagens()
    # adicionar_imagens(File("/home/villares/Área de Trabalho"))

def adicionar_imagens(selection):
    if selection == None:
        Prancha.avisos("seleção cancelada da pasta cancelada")
    else:
        Prancha.carregando = True
        dir_path = selection.getAbsolutePath()
        Prancha.path_sessao = dir_path
        Prancha.nome_sessao = unicode(selection)
        print("Pasta selecionada: " + dir_path)
        for file_name, file_path in lista_imagens(dir_path):
            img = loadImage(file_path)
            img_name = file_name.split('.')[0]
            print("imagem " + img_name + " carregada.")
            imagens[img_name.lower()] = img
            fator = Prancha.calc_fator(img)
            if not Prancha.in_pranchas(img_name):
                p = Prancha(img_name)
                p.areas.append(Area(interface.OX, interface.OY,
                                    img.width * fator, img.height * fator))
                Prancha.pranchas.append(p)

        print len(Prancha.pranchas)
        print('Número de imagens: ' + str(len(imagens)))
        Prancha.carregando = False

def salva_sessao():
    with open(join(Prancha.path_sessao, "dados.aparar"), "wb") as file:
        sessao = (Prancha.pranchas, Prancha.path_sessao)
        pickle.dump(sessao, file)
    Prancha.avisos("sessão salva em …" + unicode(Prancha.path_sessao)[-40:])


def carrega_sessao():
    from categorias import find_super_cats    
    try:
        with open(join(Prancha.path_sessao, "dados.aparar"), "rb") as file:
            Prancha.pranchas, Prancha.path_sessao = pickle.load(file)
            Area.categorias = Prancha.pranchas[0].areas[0].categorias
            Area.tags = Prancha.pranchas[0].areas[0].tags
            Area.super_cats = find_super_cats(Area.categorias)
            Prancha.avisos("sessão carregada")

    except Exception as e:
        Prancha.avisos("sessão não encontrada")
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
    

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
    # precisa salvar só a área da prancha!
    # Prancha_atual, área 0
    # png = createGraphics(w, h)
    # png.beginDraw()
    # png.image(g,-interface.OX, -inteface.OY)
    diagrama = "diagrama-" if Prancha.DIAGRAMA else "imagem-"
    nome_arquivo = diagrama + Prancha.nome_prancha_atual() + ".png"
    file = join(Prancha.path_sessao, nome_arquivo)
    saveFrame(file)
    Prancha.avisos("Imagem salva: {}".format(nome_arquivo))

def gera_csv():
    from processing.data import Table
    from collections import Counter, defaultdict
    table = Table()
    table.addColumn("AAA")
    table.addColumn("BBB")
    table.addColumn("CCC")
   
    categorias = sorted(Area.categorias.keys())
    super_cats = Area.super_cats
    print(super_cats)
    for scat in super_cats:    
        table.addColumn(scat + "_num")
        table.addColumn(scat + "_area")
    for cat in categorias:    
        table.addColumn(cat + "_num")
        table.addColumn(cat + "_area")
    
    tags = sorted(Area.tags.keys())
    for tag in tags:    
        table.addColumn(tag)
        
    for prancha in Prancha.pranchas:
        cat_count = Counter()
        scat_count = Counter()
        tag_count = Counter()
        cobertura = defaultdict(lambda: 0) 
        scobertura = defaultdict(lambda: 0) 
        nova_linha = table.addRow()
        nova_linha.setString("AAA", prancha.ida)
        nova_linha.setString("BBB", prancha.idb)
        nova_linha.setString("CCC", prancha.idc)
        
        for area in prancha.areas[1:]:  # pula o primeiro obj. Area
            if area.scat_selected:
                scat_count[area.scat_selected] += 1
                scobertura[area.scat_selected] += area.cobertura
            cat_count[area.cat_selected] += 1
            cobertura[area.cat_selected] += area.cobertura
            tag_count.update(area.tags_selected)

        for scat in super_cats:
            nova_linha.setInt(scat + "_num", scat_count[scat])
            nova_linha.setFloat(scat + "_area", scobertura[scat])            
        for cat in categorias:
            nova_linha.setInt(cat + "_num", cat_count[cat])
            nova_linha.setFloat(cat + "_area", cobertura[cat])

        for tag in tags:
            nova_linha.setInt(tag, tag_count[tag])
    
    file = join(Prancha.path_sessao, "tabela_aparar.csv")
    saveTable(table, file)
