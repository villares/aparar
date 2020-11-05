# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
from os import listdir
from os.path import isfile, join
from java.io import File

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
        print("Seleção cancelada.")
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
    print('Salvo em: ' + Prancha.path_sessao)

def carrega_sessao():
    with open(join(Prancha.path_sessao, "dados.aparar"), "rb") as file:
        Prancha.pranchas, Prancha.path_sessao = pickle.load(file)
        # if len(Prancha.pranchas) > 1:  # evita carregar sessão vazia
        #     adicionar_imagens(File(Prancha.path_sessao))

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

def gera_csv():
    from processing.data import Table
    from collections import Counter, defaultdict
    table = Table()
    table.addColumn("AAA")
    table.addColumn("BBB")
    table.addColumn("CCC")
   
    categorias = sorted(Area.categorias.keys())
    for cat in categorias:    
        table.addColumn(cat + "_num")
        table.addColumn(cat + "_area")
    tags = sorted(Area.tags.keys())
    for tag in tags:    
        table.addColumn(tag + "_area")
        
    for prancha in Prancha.pranchas:
        contador = Counter()
        cobertura = defaultdict(lambda: 0) 
        nova_linha = table.addRow()
        nova_linha.setString("AAA", self.ida)
        nova_linha.setString("BBB", self.idb)
        nova_linha.setString("CCC", self.idc)
        
        for area in prancha.areas[1:]:  # pula o primeiro obj. Area
            contador[area.cat_selected] += 1
            cobertura[area.cat_selected] += area.cobertura
            
        for cat in categorias:
            nova_linha.setInt(cat + "_num", contador[cat])
            nova_linha.setFloat(cat + "_area", cobertura[cat])
            # newRow.setString("name", "Lion")
    
    file = join(Prancha.path_sessao, "tabela_aparar.csv")
    saveTable(table, file)
