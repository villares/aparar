# -*- coding: utf-8 -*-

def setup_cats(arquivo, x, y, width_, lh):
    lines = loadStrings(arquivo)
    cat_nomes = [cat for cat in lines
                 if cat and not '(' in cat
                 and not cat.startswith('\t')]
    pos.x = pos.xo = x
    pos.y = y  # initial x and y
    cats =  {cat: {'state': False,
                  'x': pos(i, cat, width_, lh),
                  'y': pos.y,
                  'w': pos.tw,
                  'h': lh,
                  }
            for i, cat in enumerate(cat_nomes)}
    return cats

def pos(i, t, lw, lh=25, wgap=20, hgap=2):
    # set pos.x, pos.xo, pox.y before you call this
    pos.tw = textWidth(t)
    if pos.x + pos.tw > lw:
        pos.x = pos.xo
        pos.y += lh + hgap
    x = pos.x
    pos.x += pos.tw + wgap
    return x

def draw_cats(cats):
    for cat in cats:
        x, y = cats[cat]['x'], cats[cat]['y']
        w, h = cats[cat]['w'], cats[cat]['h']
        noFill()
        # rect(x, y, w, h)
        selected = cats[cat]['state']
        if selected:
            fill(200, 0, 0)
        else:
            fill(0)
        if mouse_over_cat(cat, cats):
            fill(200, 128 + 128 * selected, 128 + 128 * selected)
        text(cat, x, y + h * 0.75)
            
def seleciona_tag(cats):    
    for cat in cats:
        if mouse_over_cat(cat, cats):
            cats[cat]['state'] ^= 1

def seleciona_cat(cats):    
    for cat in cats:
        if mouse_over_cat(cat, cats):
            if cats[cat]['state']:
                cats[cat]['state'] = False
            else:
                for other in cats:
                    cats[other]['state'] = False
                cats[cat]['state'] = True

def active_cat(cats, all=False):
    if not all:
        for cat in cats:
            if cats[cat]['state']:
                return cat
        return ""
    else:
        return [cat for cat in cats if cats[cat]['state']]

def mouse_over_cat(cat, cats):
    x, y = cats[cat]['x'], cats[cat]['y']
    w, h = cats[cat]['w'], cats[cat]['h']
    return (x < mouseX < x + w
            and y < mouseY < y + h)
