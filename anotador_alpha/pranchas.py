# -*- coding: utf-8 -*-

import interface

class Prancha:

    atual = 0
    pranchas = []

    def __init__(self, nome):
        self.areas = []
        self.nome = nome

    def display_areas(self, mp):
        ma = interface.modo_ativo
        for i, a in reversed(list(enumerate(self.areas))):
            if a.mouse_over() and ma != interface.CRIAR:
                if i != 0:
                    a.over = True
                    if ma == interface.REMOV:
                        a.selected = True
                elif ma == interface.MOVER:                    
                    a.over = True
                break
            elif ma == interface.REMOV:
                a.selected = False
        
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
        fator = float(height - 100) / img.height
        image(img, interface.ox, interface.oy,
              img.width * fator, img.height * fator)

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
