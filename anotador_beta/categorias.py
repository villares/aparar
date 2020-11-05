# -*- coding: utf-8 -*-

def setup_terms(arquivo, x, y, width_, lh):
    lines = loadStrings(arquivo)
    term_names = [term for term in lines
                 if term and not '(' in term
                 and not term.startswith('\t')]
    pos.x = pos.xo = x
    pos.y = y  # initial x and y
    terms =  {term: {'state': False,
                  'x': pos(i, term, width_, lh),
                  'y': pos.y,
                  'w': pos.tw,
                  'h': lh,
                  }
            for i, term in enumerate(term_names)}
    return terms

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

def draw_terms(terms):
    for term in terms:
        x, y = terms[term]['x'], terms[term]['y']
        w, h = terms[term]['w'], terms[term]['h']
        noFill()
        # rect(x, y, w, h)
        selected = terms[term]['state']
        if selected:
            fill(200, 0, 0)
        else:
            fill(0)
        if mouse_over_term(term, terms):
            fill(200, 128 + 128 * selected, 128 + 128 * selected)
        text(term, x, y + h * 0.75)
            
def select_tag(terms):    
    for term in terms:
        if mouse_over_term(term, terms):
            terms[term]['state'] ^= 1

def select_cat(terms):    
    for term in terms:
        if mouse_over_term(term, terms):
            if terms[term]['state']:
                terms[term]['state'] = False
            else:
                for other in terms:
                    terms[other]['state'] = False
                terms[term]['state'] = True

def active_term(terms, all=False):
    if not all:
        for term in terms:
            if terms[term]['state']:
                return term
        return ""
    else:
        return [term for term in terms if terms[term]['state']]

def mouse_over_term(term, terms):
    x, y = terms[term]['x'], terms[term]['y']
    w, h = terms[term]['w'], terms[term]['h']
    return (x < mouseX < x + w
            and y < mouseY < y + h)
