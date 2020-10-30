# -*- coding: utf-8 -*-

import interface

class Prancha:

    atual = 0
    pranchas = []

    def __init__(self, nome):
        self.areas = []
        self.nome = nome       # AAA_BBB_CCCxxxxxx
        self.ida = nome[:3]    # AAA
        self.idb = nome[4:7]   # BBB
        self.idc = nome[8:11]  # CCC
        print(self.ida, self.idb, self.idc)

    def display_areas(self, mp):
        ma = interface.modo_ativo
        if ma == interface.REMOV:
            Prancha.desselect_all()
        for i, a in reversed(list(enumerate(self.areas))):
            if a.mouse_over() and ma != interface.CRIAR:
            # mouse sobre, exceto no modo CRIAR
                if i != 0:  # exceto para a primeira área
                    a.over = True
                    if ma == interface.REMOV:
                        a.selected = True  # destaque extra no REMOV
                        break
                elif ma == interface.MOVER:
                    # primeira área destaca com mouse over par MOVER
                    a.over = True
                break

        self.update()
        for a in reversed(self.areas):
            a.display(mp)

    def update(self):
        a0 = self.areas[0]
        for a in self.areas:
            a.area = a.w * a.h
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
        if nome != 'home':
            fill(200, 0, 0)
            texto = "({:03}/{:03}) {}".format(cls.atual, total, nome)
            text(texto, width / 2, 30)
        else:
            fill(0)
            text("({}) carregadas".format(total), width / 2, 30)

    @classmethod
    def nome_prancha_atual(cls):
        return cls.pranchas[cls.atual].nome

    @classmethod
    def display_imagem_atual(cls, imagens):
        img = imagens[cls.nome_prancha_atual().lower()]
        fator = cls.calc_fator(img)
        image(img, interface.ox, interface.oy,
              img.width * fator, img.height * fator)

    @classmethod
    def calc_fator(cls, img):
        return float(height - (interface.oy + interface.rodape)) / img.height


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
