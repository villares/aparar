# -*- coding: utf-8 -*
from __future__ import unicode_literals

from copy import deepcopy
from categorias import  * #draw_terms, select_cat, select_tag, active_term
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
        self.tags = deepcopy(Area.tags)
        self.tags_state = setup_terms_state(Area.tags) #*
        self.categorias = deepcopy(Area.categorias)
        self.categorias_state = setup_terms_state(Area.categorias) #*
        self.cat_selected = ""
        self.scat_selected = None
        self.tags_selected = []

    def display(self, mp):
        textSize(CAT_FONT_SIZE)
        stroke(0)
        fill(0)
        if self.selected:
            stroke(200, 0, 0)
            strokeWeight(3)
            not_remove_mode = interface.modo_ativo != interface.REMOV
            if (self.cobertura != 1 and not_remove_mode):
                draw_terms(self.categorias)
                draw_terms(self.tags)
        elif self.over and not mp:
            strokeWeight(5)
            self.over = False
        else:
            strokeWeight(2)
        self.cat_selected = active_term(self.categorias)
        sep_pos = self.cat_selected.find("-")
        if  sep_pos > 0:
            self.scat_selected = self.cat_selected[:sep_pos]
        else:
            self.scat_selected = None 
        self.tags_selected = active_term(self.tags, all=True)
        fill(0)
        text(self.cat_selected, self.x + 10, self.y + 20)
        pushStyle()
        textAlign(CENTER, CENTER)
        textSize(AREA_FONT_SIZE)
        text("{:2.0%}".format(self.cobertura),
             self.x + self.w / 2, self.y + self.h - 20)
        fill(0, 20)
        rect(self.x, self.y, self.w, self.h)
        popStyle()


    def cat_and_tag_selection(self):
        select_cat(self.categorias)
        select_tag(self.tags)

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w
                and self.y < mouseY < self.y + self.h)
