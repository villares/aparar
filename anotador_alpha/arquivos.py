# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
from os import listdir
from os.path import isfile, join
from java.io import File

from pranchas import Prancha
from areas import Area

imagens = {}

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
    selectFolder("Selecione uma pasta", "adicionar_imagens")

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
            if not Prancha.in_pranchas(img_name):
                p = Prancha(img_name)
                p.areas.append(Area(Prancha.ox, Prancha.oy,
                                    img.width * fator, img.height * fator))
                Prancha.pranchas.append(p)

        print len(Prancha.pranchas)
        print('Número de imagens: ' + str(len(imagens)))

def salva_sessao():
    with open(join(sketchPath('data'), "aparar_session.pickle"), "wb") as file:
        sessao = (Prancha.pranchas, Prancha.path)
        pickle.dump(sessao, file)
    print('Salvo em: ' + sketchPath('data'))
    
def carrega_sessao():
    with open(join(sketchPath('data'), "aparar_session.pickle"), "rb") as file:
        Prancha.pranchas, Prancha.path = pickle.load(file)
        adicionar_imagens(File(Prancha.path))

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
