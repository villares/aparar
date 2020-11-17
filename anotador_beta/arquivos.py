# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from processing.data import Table
from collections import Counter, defaultdict
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
            return True

    except Exception as e:
        Prancha.avisos("não encontrados dados de sessão salva")
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
    # Para salvar só a área 100 % da prancha
    saveFrame("temp.png")  # salva arquivo temporário da tela toda
    temp = loadImage("temp.png")
    png = createGraphics(w, h)
    png.beginDraw()
    png.background(255)
    png.copy(temp, x + 1, y + 1, w, h, 0, 0, w, h)
    png.save(path_arquivo)  # salva arquivo só com o conteúdo da área do 100%
    png.endDraw()
    Prancha.avisos("Imagem salva: {}".format(nome_arquivo))

def reset_acumulador():
    global t_cat_count, t_scat_count, t_tag_count, t_cobertura, t_scobertura
    t_cat_count = Counter()
    t_scat_count = Counter()
    t_tag_count = Counter()
    t_cobertura = defaultdict(lambda: 0)
    t_scobertura = defaultdict(lambda: 0)

def gera_csv():
    table = Table()
    table.addColumn("AAA")
    table.addColumn("BBB")
    table.addColumn("CCC")
    categorias = sorted(Area.categorias.keys())
    for cat in categorias:
        table.addColumn(cat + "_num")
        table.addColumn(cat + "_area")
    super_cats = Area.super_cats
    for scat in super_cats:
        table.addColumn(scat + "_num")
        table.addColumn(scat + "_area")
    tags = sorted(Area.tags.keys())
    for tag in tags:
        table.addColumn(tag)

    prancha_atual = "000"
    linhas_iguais = 0
    reset_acumulador()

    for prancha in Prancha.pranchas:
        if prancha_atual != (prancha.ida, prancha.idb):
            if prancha_atual != "000" and linhas_iguais > 1:
                t_nova_linha = table.addRow()
                t_nova_linha.setString("AAA", prancha_atual[0])
                t_nova_linha.setString("BBB", prancha_atual[1])
                t_nova_linha.setString("CCC", "TOTAL")
                write_linha(t_nova_linha, super_cats, t_scat_count, t_scobertura,
                            categorias, t_cat_count, t_cobertura,
                            tags, t_tag_count)
            prancha_atual = (prancha.ida, prancha.idb)
            linhas_iguais = 1
            reset_acumulador()
        else:
            linhas_iguais += 1

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
                t_scat_count[area.scat_selected] += 1
                scobertura[area.scat_selected] += area.cobertura
                t_scobertura[area.scat_selected] += area.cobertura
            cat_count[area.cat_selected] += 1
            t_cat_count[area.cat_selected] += 1
            cobertura[area.cat_selected] += area.cobertura
            t_cobertura[area.cat_selected] += area.cobertura
            tag_count.update(area.tags_selected)
            t_tag_count.update(area.tags_selected)

        write_linha(nova_linha, super_cats, scat_count, scobertura,
                    categorias, cat_count, cobertura,
                    tags, tag_count)

    file = join(Prancha.path_sessao, "tabela_aparar.csv")
    saveTable(table, file)
    Prancha.avisos("CSV salvo em …" + unicode(Prancha.path_sessao)[-40:])


def write_linha(nova_linha, super_cats, scat_count, scobertura,
                categorias, cat_count, cobertura,
                tags, tag_count):
    for scat in super_cats:
        nova_linha.setInt(scat + "_num", scat_count[scat])
        nova_linha.setFloat(scat + "_area", scobertura[scat])
    for cat in categorias:
        nova_linha.setInt(cat + "_num", cat_count[cat])
        nova_linha.setFloat(cat + "_area", cobertura[cat])
    for tag in tags:
        nova_linha.setInt(tag, tag_count[tag])
