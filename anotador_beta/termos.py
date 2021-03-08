# -*- coding: utf-8 -*-

from collections import OrderedDict

import interface

# arquivos com as categorias e tags iniciais
CATEGORIAS_TXT, TAGS_TXT = "categorias.txt", "tags.txt"

def criar_categorias(strings=None):
    strings = strings or loadStrings(CATEGORIAS_TXT)
    nomes = list(OrderedDict.fromkeys(strings))      # remove duplicações mas mantém a ordem
    categorias = setup_terms(nomes,       # nomes das categorias
                                        interface.MENU_OX, # x_inicial
                                        interface.OY + interface.MENU_V_SPACE * 13, # y_inicial
                                        interface.OX - 10,                          # w
                                        interface.TERM_FONT_SIZE + 2)               # h
    super_cats = find_super_cats(categorias)
    return categorias, super_cats
    
def criar_tags(strings=None):
    strings = strings or loadStrings(TAGS_TXT)
    nomes = list(OrderedDict.fromkeys(strings))      # remove duplicações mas mantém a ordem
    tags = setup_terms(nomes,             # nomes dos tags
                                  20 + interface.OX,              # x_inicial
                                  4 + height - interface.rodape,  # y_inicial
                                  width - 20, interface.TERM_FONT_SIZE + 2, wgap=10)  # w, h, wgap: espaço entre tags 
    return tags

def setup_terms(strings, x, y, width_, lh, wgap=20, hgap=2):
    term_names = [term for term in strings
                  if term and not '(' in term
                  and not term.startswith('\t')]
                  
    def pos(i, t, lw, lh=25, wgap=20, hgap=2):
        # set pos.x, pos.xo, pox.y before you call this
        textSize(interface.TERM_FONT_SIZE)
        pos.tw = textWidth(t)
        if pos.x + pos.tw > lw:
            pos.x = pos.xo
            pos.y += lh + hgap
        x = pos.x
        pos.x += pos.tw + wgap
        return x              
    
    # x and y for first term             
    pos.x = pos.xo = x
    pos.y = y  
    terms = OrderedDict((term, {'x': pos(i, term, width_, lh, wgap, hgap),
                                'y': pos.y,
                                'w': pos.tw,
                                'h': lh,
                                'id_cor': int(255.0 /  len(term_names) * i) 
                               })
                         for i, term in enumerate(term_names))
    return terms

def setup_terms_state(terms):
    return {term: False for term in terms.keys()}

def find_super_cats(cats):
    supers = set()
    for cat in cats:
        sep_pos = cat.find("-")
        if sep_pos > 0:
            supers.add(cat[:sep_pos])
    return sorted(list(supers))

def draw_terms(terms, terms_state=None, DEBUG=False):
    for term in terms:
        x, y = terms[term]['x'], terms[term]['y']
        w, h = terms[term]['w'], terms[term]['h']
        if DEBUG:
            pushStyle()
            noFill()
            strokeWeight(1)
            rect(x, y, w, h)
            popStyle()
        selected = terms_state.get(term, False)
        if selected:
            fill(200, 0, 0)
        else:
            fill(0)
        if mouse_over_term(term, terms):
            fill(200, 128 + 128 * selected, 128 + 128 * selected)
        text(term, x, y)

def select_tag(terms, terms_state):
    for term in terms:
        if mouse_over_term(term, terms):
                terms_state[term] = not terms_state.get(term, False)

def select_cat(terms, terms_state):
    for term in terms:
        if mouse_over_term(term, terms):
                if terms_state.get(term):
                    terms_state[term] = False
                else:
                    for other in terms:
                        terms_state[other] = False
                    terms_state[term] = True

def active_term_state(terms_state, all=False):
    all_active = [term for term in terms_state if terms_state.get(term)]
    if all:
        return all_active
    else:
        if len(all_active) == 0:
            return ""
        else:
            return all_active[0]

def mouse_over_term(term, terms):
    x, y = terms[term]['x'], terms[term]['y']
    w, h = terms[term]['w'], terms[term]['h']
    return (x < mouseX < x + w and
            y < mouseY < y + h)
