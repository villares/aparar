# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import interface

class Prancha:

    atual = 0
    pranchas = []
    path_sessao = ""
    nome_sessao = ""
    carregando = False

    def __init__(self, nome):
        self.areas = []
        self.nome = nome       # AAA_BBB_CCCxxxxxx
        sep_pos = nome.find("_")
            if sep_pos > 0:
               self.ida = nome[:sep_pos]    # AAA ou AAAA
               self.idb = nome[sep_pos:sep_pos+3]   # BBB
               self.idc = nome[sep_pos+3:sep_pos+6]  # CCC
            else:
                self.ida = self.idb = self.idc = nome

    def display_areas(self, mp):
        ma = interface.modo_ativo
        if ma == interface.REMOV:
            Prancha.desselect_all()
        for i, a in reversed(list(enumerate(self.areas))):
            if a.mouse_over() and ma != interface.CRIAR:
            # mouse sobre, exceto no modo CRIAR
                if i != 0:  # exceto para 1° obj. Area
                    a.over = True
                    if ma == interface.REMOV:
                        a.selected = True  # destaque extra no REMOV
                        break
                elif ma == interface.EDITA:
                    # 1° obj. Area destaca com mouse over para MOVER
                    a.over = True
                break

        self.update()  # atualiza cálculo de áreas dos objetos Area
        for a in reversed(self.areas):
            a.display(mp)

    def update(self):
        """Recalcule areas e % de cobertura dos obj. Area desta prancha."""
        a0 = self.areas[0]  # primeiro obj. Area define 100% de cobertura
        for a in self.areas:
            a.area = a.w * a.h  # atualiza area
            if a != a0:
                a.cobertura = a.area / float(a0.area)

    @classmethod
    def in_pranchas(cls, nome):
        return nome in cls.get_names()

    @classmethod
    def get_names(cls):
        return [p.nome for p in cls.pranchas]

    @classmethod
    def display_nome_atual(cls):
        nome = cls.nome_prancha_atual()
        total = len(cls.pranchas) - 1  # home não conta!
        if nome != '000':  # prancha "home" teste
            fill(200, 0, 0)
            texto = "({:03}/{:03}) {}".format(cls.atual, total, nome)
            text(texto, width / 2, 30)
        else:
            fill(0)
            text("({}) pranchas carregadas".format(total), width / 2, 30)

    @classmethod
    def nome_prancha_atual(cls):
        return cls.pranchas[cls.atual].nome

    @classmethod
    def display_imagem_atual(cls, imagens):
        img = imagens.get(cls.nome_prancha_atual().lower())
        if img is not None:
            fator = cls.calc_fator(img)
            image(img, interface.OX, interface.OY,
                img.width * fator, img.height * fator)
        else:
            cls.avisos("IMAGEM NÃO CARREGADA")
            
    @classmethod
    def calc_fator(cls, img):
        return float(height - (interface.OY + interface.rodape)) / img.height


    @classmethod
    def display_areas_atual(cls, mp):
        cls.pranchas[cls.atual].display_areas(mp)

    @classmethod
    def get_areas_atual(cls):
        return cls.pranchas[cls.atual].areas

    @classmethod
    def desselect_all(cls):
        for r in cls.get_areas_atual():
            r.selected = False
            
    @classmethod        
    def avisos(cls, t=None):
        if cls.carregando:
            t = "CARREGANDO IMAGENS"
        if t:
            push()
            fill(200, 0, 0)
            textSize(24)
            text(t, width / 2, height / 2)
            pop()
