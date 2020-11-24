# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from processing.data import Table
from collections import Counter, defaultdict

from pranchas import Prancha
from areas import Area
from os.path import join


NOME_PLANILHA = "planilha_aparar_v1124.csv"
NOME_PLANILHA2 = "planilha_aparar_expandida_v1124.csv"

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
                            tags, t_tag_count, linhas_iguais)
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
    print Prancha.path_sessao    
    file = join(Prancha.path_sessao, NOME_PLANILHA)
    saveTable(table, file)
    Prancha.avisos("CSV salvo em …" + unicode(Prancha.path_sessao)[-40:])

def gera_csv2():
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
                            tags, t_tag_count, linhas_iguais)
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

    file = join(Prancha.path_sessao, NOME_PLANILHA2)
    saveTable(table, file)
    Prancha.avisos("CSV salvo em …" + unicode(Prancha.path_sessao)[-40:])
    
def write_linha(nova_linha, super_cats, scat_count, scobertura,
                categorias, cat_count, cobertura,
                tags, tag_count, num_pranchas=1):
    for scat in super_cats:
        nova_linha.setInt(scat + "_num", scat_count[scat])
        nova_linha.setFloat(scat + "_area", scobertura[scat] / num_pranchas)
    for cat in categorias:
        nova_linha.setInt(cat + "_num", cat_count[cat])
        nova_linha.setFloat(cat + "_area", cobertura[cat] / num_pranchas)
    for tag in tags:
        nova_linha.setInt(tag, tag_count[tag])
        
def reset_acumulador():
    global t_cat_count, t_scat_count, t_tag_count, t_cobertura, t_scobertura
    t_cat_count = Counter()
    t_scat_count = Counter()
    t_tag_count = Counter()
    t_cobertura = defaultdict(lambda: 0)
    t_scobertura = defaultdict(lambda: 0)
