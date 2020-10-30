def draw_cats():
    for cat in cats:
        x, y = cats[cat]['x'], cats[cat]['y']
        w, h = cats[cat]['w'], cats[cat]['h']
        noFill()
        # rect(x, y, w, h)
        selected = cats[cat]['state']
        if selected:
            fill(255)
        else:
            fill(0)
        if mouse_over_cat(cat):
            fill(255, 128 * selected, 128 * selected)
        text(cat, x, y + h * 0.75)
    
def seleciona_tag(cats):    
    for cat in cats:
        if mouse_over_cat(cat):
            cats[cat]['state'] ^= 1

def seleciona_cat(cats):    
    for cat in cats:
        if mouse_over_cat(cat):
            cats[cat]['state'] = True
        else:
            cats[cat]['state'] = False



def mouse_over_cat(cat):
    x, y = cats[cat]['x'], cats[cat]['y']
    w, h = cats[cat]['w'], cats[cat]['h']
    return (x < mouseX < x + w
            and y < mouseY < y + h)

def pos(i, t, lw, lh=25, wgap=20):
    # set pos.x, pos.xo, pox.y before you call this
    pos.tw = textWidth(t)
    if pos.x + pos.tw > lw:
        pos.x = pos.xo
        pos.y += lh
    x = pos.x
    pos.x += pos.tw + wgap
    return x

def setup_cats(arquivo, x, y, width_):
    lines = loadStrings(arquivo)
    cat_nomes = [cat for cat in lines[200:]
                 if cat and not '(' in cat
                 and not cat.startswith('\t')]
    pos.x = pos.xo = x
    pos.y = y  # initial x and y
    return {cat: {'state': False,
                  'x': pos(i, cat, width_),
                  'y': pos.y,
                  'w': pos.tw,
                  'h': 20,
                  }
            for i, cat in enumerate(cat_nomes)}
