# -*- coding: utf-8 -*-

def setup_terms(arquivo, x, y, width_, lh, wgap=20, hgap=2):
    lines = loadStrings(arquivo)
    term_names = [term for term in lines
                  if term and not '(' in term
                  and not term.startswith('\t')]
    pos.x = pos.xo = x
    pos.y = y  # initial x and y
    terms = {term: {
                    'x': pos(i, term, width_, lh, wgap, hgap),
                    'y': pos.y,
                    'w': pos.tw,
                    'h': lh,
                    'cor' : calc_cat_color(i, len(term_names)) 
                    }
             for i, term in enumerate(term_names)}
    return terms

def calc_cat_color(i, num_terms, transparencia=155):
    m = int(255.0 / num_terms * i)
    colorMode(HSB)
    # c = color(m, 128 + 128 * (m % 2), 255 - 128 * (m % 3), transparencia)
    c = color(m, 255 - (i % 2) * 64 , 255 - (i % 3) * 64, transparencia)
    colorMode(RGB)
    return c 

def setup_terms_state(terms):
    return {term: False for term in terms.keys()}

def find_super_cats(cats):
    supers = set()
    for cat in cats:
        sep_pos = cat.find("-")
        if sep_pos > 0:
            supers.add(cat[:sep_pos])
    return sorted(list(supers))

def pos(i, t, lw, lh=25, wgap=20, hgap=2):
    # set pos.x, pos.xo, pox.y before you call this
    pos.tw = textWidth(t)
    if pos.x + pos.tw > lw:
        pos.x = pos.xo
        pos.y += lh + hgap
    x = pos.x
    pos.x += pos.tw + wgap
    return x

def draw_terms(terms, terms_state=None):
    for term in terms:
        x, y = terms[term]['x'], terms[term]['y']
        w, h = terms[term]['w'], terms[term]['h']
        noFill()
        # rect(x, y, w, h)
        selected = terms_state[term] # if terms_state else terms[term]['state']
        if selected:
            fill(200, 0, 0)
        else:
            fill(0)
        if mouse_over_term(term, terms):
            fill(200, 128 + 128 * selected, 128 + 128 * selected)
        text(term, x, y + h * 0.75)

def select_tag(terms, terms_state):
    for term in terms:
        if mouse_over_term(term, terms):
                terms_state[term] ^= 1

def select_cat(terms, terms_state):
    for term in terms:
        if mouse_over_term(term, terms):
                if terms_state[term]:
                    terms_state[term] = False
                else:
                    for other in terms:
                        terms_state[other] = False
                    terms_state[term] = True

def active_term_state(terms_state, all=False):
    if not all:
        for term in terms_state.keys():
            if terms_state[term]:
                return term
        return ""
    else:
        return [term for term in terms_state if terms_state[term]]

def mouse_over_term(term, terms):
    x, y = terms[term]['x'], terms[term]['y']
    w, h = terms[term]['w'], terms[term]['h']
    return (x < mouseX < x + w
            and y < mouseY < y + h)
