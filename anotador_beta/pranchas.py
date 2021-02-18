# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import interface

class Prancha:

    i_atual = 0
    pranchas = []
    path_sessao = ""
    nome_sessao = ""
    carregando = False  # remover na próxima mudança de formato de arquivo
    avisos_timer = 0
    avisos_texto = ""

    def __init__(self, nome):
        self.areas = []
        self.nome = nome       # AAA_BBB_CCCxxxxxx
        self.init_ids()
        self.rot = 0

    def init_ids(self):
        nome = self.nome.replace("-", "_")
        count_sep = self.nome.count("_")        
        if count_sep >= 2:
            ids = nome.split("_")
            self.ida = nome[0]      # AAA ou qualquer número de caracteres antes do primeiro _
            self.idb = nome[1]      # BBB ou qualquer número de caracteres antes do segundo _
            self.idc = nome[2][:3]  # CCC (3 caracteres)
        else:
            if nome != "000":
                println(nome + " (nome da imagem não está no padrão)")
            self.ida = self.idb = self.idc = nome

    def id_a_b(self):
        return self.ida + "_" + self.idb

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
    def load_img_prancha_atual(cls, imagens):
        """devolve imagem na prancha atual ou None"""
        path_img = imagens.get(cls.nome_prancha_atual().lower())
        if path_img:
            return loadImage(path_img)
        else:
            return createGraphics(10, 10)

    @classmethod
    def display_imagem_atual(cls, imagens):
        img, rot, fator = cls.imagem_rot_fator_atual()
        if img:
            image_rot(img, rot, interface.OX, interface.OY,
                      img.width * fator, img.height * fator)
        else:
            cls.avisos("IMAGEM NÃO CARREGADA")

    @classmethod
    def imagem_rot_fator_atual(cls):
        img = interface.imagem_prancha_atual
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
    def calc_correction_factor(self):
        """para ajustar no caso de mudança de tela"""
        current_height = height - (interface.OY + interface.rodape)
        return current_height / self.screen_height

    @classmethod
    def update_for_name_change(cls):
        for prancha in cls.pranchas:
            # para o caso da sessão salva com nomes com hifens
            prancha.init_ids()

    @classmethod
    def update_for_screen_change(cls):
        current_height = height - (interface.OY + interface.rodape)
        recorded_height = Prancha.screen_height
        if current_height != recorded_height:
            print("update for screen change")
            dy = current_height - recorded_height
            cf = Prancha.calc_correction_factor()
            print int(recorded_height) * cf, current_height
            Prancha.screen_height = current_height
            for prancha in cls.pranchas:
                for area in prancha.areas:
                    area.x = (area.x - interface.OX) * cf + interface.OX
                    area.y = (area.y - interface.OY) * cf + interface.OY
                    area.w *= cf
                    area.h *= cf
                    for tag in area.tags:
                        area.tags[tag]['y'] += dy
        else:
            print "no change"

    @classmethod
    def display_areas_atual(cls, mp):
        cls.pranchas[cls.i_atual].display_areas(mp)

    @classmethod
    def get_areas_atual(cls):
        return cls.pranchas[cls.i_atual].areas

    @classmethod
    def desselect_all(cls):
        for a in cls.get_areas_atual():
            a.selected = False

    @classmethod
    def desselect_all_in_all(cls):
        for p in cls.pranchas:
            for a in p.areas:
                a.selected = False

    @classmethod
    def avisos(cls, message=None):

        if message and cls.avisos_timer == 0:
            cls.avisos_texto = message
            cls.avisos_timer = millis()
        # elif cls.carregando:
        #     cls.avisos_texto = "CARREGANDO IMAGENS"
        # cls.avisos_timer = millis()
        # cls.carregando = False

        if millis() - cls.avisos_timer > 1200:
            cls.avisos_texto = t = ""
            cls.avisos_timer = 0

        t = cls.avisos_texto

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
