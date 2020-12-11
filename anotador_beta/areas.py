# -*- coding: utf-8 -*
from __future__ import unicode_literals

from copy import deepcopy
from categorias import *  # draw_terms, select_cat, select_tag, active_term
from pranchas import Prancha
import interface

AREA_FONT_SIZE = 18
CAT_FONT_SIZE = 11

class Area:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.selected = False
        self.over = False
        self.area = self.w * self.h
        self.cobertura = 1  # 100%
        self.tags_state = setup_terms_state(Area.tags)  # *
        self.categorias_state = setup_terms_state(Area.categorias)  # *
        self.cat_selected = ""
        self.scat_selected = None
        self.tags_selected = []

    def update(self):
        # atualiza qual categoria desta área
        self.cat_selected = active_term_state(self.categorias_state)
        # atualiza, se tiver, supercategoria (categoria-prefixo)
        sep_pos = self.cat_selected.find("-")
        if sep_pos > 0:
            self.scat_selected = self.cat_selected[:sep_pos]
        else:
            self.scat_selected = None
        # atualiza lista de tags que estão selecionados
        self.tags_selected = active_term_state(self.tags_state, all=True)

    def display(self, mp):
        self.update()
        modo_anotativo = interface.modo_ativo in (
            interface.EDITA, interface.CRIAR)
        modo_diagrama = interface.modo_ativo == interface.DIAGR
        pushStyle()
        textSize(CAT_FONT_SIZE)
        stroke(0)
        if self.selected and self.cobertura != 1:
            stroke(200, 0, 0)
            strokeWeight(3)
            if modo_anotativo:
                draw_terms(Area.categorias, self.categorias_state)
                draw_terms(Area.tags, self.tags_state)
        elif self.over and self.cobertura != 1:  # not mp: # and :
            strokeWeight(5)
            self.over = False
        else:
            strokeWeight(2)
        # pega dados da categoria que está selecionada (se houver)
        cat = Area.categorias.get(self.cat_selected)
        if cat and modo_diagrama:
            fill(cat['cor'])
            noStroke()
        else:  # senão usa cinza translúcido padrão
            fill(0, 20)
        # caso especial do modo de editar área de referência 100%
        if interface.modo_ativo == interface.ED100:
            if self.cobertura == 1:
                stroke(200, 0, 0)
                strokeWeight(5)
            else:
                stroke(0)
                strokeWeight(3)
        # desenha o retângulo da área
        rect(self.x, self.y, self.w, self.h)
        fill(0)  # textos da área em preto
        # push()
        # translate(self.x + self.w / 2, self.y + self.h / 2)
        # rotate(self.rotation)
        # rect(-self.w / 2, -self.h / 2, self.w, self.h)
        # pop()
        # fill(0)  # textos da área em preto
        if not modo_diagrama:
            text(self.cat_selected,
                 self.x + 10,
                 self.y + 20)
        textAlign(CENTER, CENTER)
        textSize(AREA_FONT_SIZE)
        # caso da área de referência 100% (cobertura == 1)
        if self.cobertura == 1 and modo_diagrama:
            text(Prancha.nome_prancha_atual(),
                 self.x + self.w / 2,
                 self.y + self.h - 20)
        else:
            text("{:2.0%}".format(self.cobertura),
                 self.x + self.w / 2,
                 self.y + self.h - 20)
        popStyle()

    def cat_and_tag_selection(self):
        if self.cobertura != 1:  # menos para a àrea de ref. 100%
            select_cat(Area.categorias, self.categorias_state)
            select_tag(Area.tags, self.tags_state)

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w
                and self.y < mouseY < self.y + self.h)

    @classmethod
    def calc_color(cat_name):
        cat = cls.categorias.get(cat_name)
        if cat:
            c = cat['cor']
            return color(c, 128 + 128 * (c % 2), 255 - 128 * (c % 3), 155)
