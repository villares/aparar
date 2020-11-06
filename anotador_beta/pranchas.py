# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import interface

class Prancha:

    i_atual = 0
    pranchas = []
    path_sessao = ""
    nome_sessao = ""
    carregando = False

    def __init__(self, nome):
        self.areas = []
        self.nome = nome       # AAA_BBB_CCCxxxxxx
        self.init_ids()
        self.rot = 0

    def init_ids(self):
        nome = self.nome
        sep_pos = nome.find("_")
        if sep_pos > 0:
            self.ida = nome[:sep_pos]    # AAA ou AAAA
            self.idb = nome[sep_pos:sep_pos + 3]   # BBB
            self.idc = nome[sep_pos + 3:sep_pos + 6]  # CCC
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
            texto = "({:03}/{:03}) {}".format(cls.i_atual, total, nome)
        else:
            fill(0)
            texto = "pranchas carregadas: {}".format(total)
        text(texto, 780, 30)

    @classmethod
    def nome_prancha_atual(cls):
        return cls.pranchas[cls.i_atual].nome

    @classmethod
    def img_prancha_atual(cls, imagens):
        """devolve imagem na prancha atual ou None"""
        return imagens.get(cls.nome_prancha_atual().lower())

    @classmethod
    def display_imagem_atual(cls, imagens):
        img, rot, fator = cls.imagem_rot_fator_atual(imagens)
        if img:
            image_rot(img, rot, interface.OX, interface.OY,
                      img.width * fator, img.height * fator)
        else:
            cls.avisos("IMAGEM NÃO CARREGADA")

    @classmethod
    def imagem_rot_fator_atual(cls, imagens):
        img = cls.img_prancha_atual(imagens)
        if img:
            rot = cls.pranchas[cls.i_atual].rot
            fator = cls.calc_fator(img, rot == 1 or rot == 3)
            return img, rot, fator
        else:
            return None, None, None

    @classmethod
    def calc_fator(cls, img, rotated=False):
        if not rotated:
            return float(height - (interface.OY + interface.rodape)) / img.height
        else:
            return float(height - (interface.OY + interface.rodape)) / img.width

    @classmethod
    def display_areas_atual(cls, mp):
        cls.pranchas[cls.i_atual].display_areas(mp)

    @classmethod
    def get_areas_atual(cls):
        return cls.pranchas[cls.i_atual].areas

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
            text(t, interface.OX + 10, interface.OY + 30)
            pop()


def image_rot(img, rot, x, y, w=None, h=None):
    w = w or img.width
    h = h or img.height
    pushMatrix()
    if rot == 1:
        translate(x + h, y)
        rotate(HALF_PI)
        image(img, 0, 0, w, h)
    elif rot == 2:
        translate(x + w, y + h)
        rotate(PI)
        image(img, 0, 0, w, h)
    elif rot == 3:
        translate(x, y + w)
        rotate(HALF_PI + PI)
        image(img, 0, 0, w, h)
    else:
        image(img, x, y, w, h)
    popMatrix()
