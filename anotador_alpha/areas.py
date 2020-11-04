# -*- coding: utf-8 -*
from __future__ import unicode_literals

from copy import deepcopy
from categorias import draw_cats, seleciona_cat, seleciona_tag, active_cat
import interface

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
        self.tags = deepcopy(Area.tags)
        self.categorias = deepcopy(Area.categorias)
        self.cat = ""

    def display(self, mp):
        textSize(11)
        stroke(0)
        fill(0)
        if self.selected:
            stroke(200, 0, 0)
            fill(100, 0, 0)
            strokeWeight(3)
        elif self.over and not mp:
            strokeWeight(5)
            self.over = False
        else:
            strokeWeight(2)
        self.cat = active_cat(self.categorias)
        text('{} ({:2.0%})'.format(self.cat, self.cobertura),
             self.x + 10, self.y + 20)
        fill(0, 20)
        rect(self.x, self.y, self.w, self.h)

        ma = interface.interface.modo_ativo
        if (self.cobertura != 1 and self.selected and
                ma in (interface.SELEC, interface.CRIAR)):
            draw_cats(self.categorias)
            draw_cats(self.tags)

    def cat_and_tag_selection(self):
        seleciona_cat(self.categorias)
        seleciona_tag(self.tags)

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w
                and self.y < mouseY < self.y + self.h)
