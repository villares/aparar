# -*- coding: utf-8 -*-

import interface #import categorias, tags, input_pane, recria_categorias, recria_tags
from termos import mouse_over_term

context_menu_clicked = None


def desenha():
    global context_menu
    context_menu = (
        {"name": "create", "x": 20, "y": 0, "func": create},
        {"name": "rename", "x": 20, "y": 20, "func": rename},
        {"name": "delete", "x": 20, "y": 40, "func": delete},
    )
    push()
    textAlign(LEFT, CENTER)
    if context_menu_clicked:
        x, y, item = context_menu_clicked
        draw_interface_elements(context_menu, x, y)
    pop()
    
def create(item):
    sugestao = 'Nova categoria'
    novo_nome = interface.input_pane(question='Novo termo',
                           suggestion=sugestao)
    if novo_nome:
        novas_categorias = interface.categorias.keys() + [novo_nome.strip()]

def rename(picked_item):
    if picked_item:
        novo_nome = input_pane(question='Rename {} to?'.format(picked_item['name']),
                         suggestion=picked_item['name'])
        # if novo_nome: 
        #     picked_item['name'] = novo_nome
    
def delete(picked_item):
    if picked_item in categoria.keys():
            # main_menu.remove(picked_item)
            # recria(main_menu)
            return

def draw_interface_elements(menu_items, x_offset=0, y_offset=0):
    for item in menu_items:
        if item_disabled(item):
            fill(128)  # Dark grey for diabled
            return # nem desenha
        elif mouse_over(x_offset, y_offset, item):
            fill(255)  # White for mouse over
        elif context_menu_clicked and context_menu_clicked[-1] == item:
            fill(240)  # Light grey if picked with right button
        else:
            fill(0)    # otherwise black
        text(item['name'], x_offset + item['x'], y_offset + item['y'])
  
def item_disabled(item):
    if context_menu_clicked:
        picked_item = context_menu_clicked[-1]
        if item['name'] == 'create':
            return False  # Create is always available
        elif picked_item == None:
            return True   # Other items unavailable if nothing picked
        else:
            return False  # otherwise they are available
    else:
        return False # nothing is disabled if context_menu_clicked is False
            
def mouse_clicked(mb):
    global context_menu_clicked
    for k in interface.categorias.keys():
        if mouse_over_term(k, interface.categorias):
            item = k
        else:
            item = None
    if mb == RIGHT and not context_menu_clicked:
        context_menu_clicked = (mouseX, mouseY, item)
    elif context_menu_clicked:
        x, y, item = context_menu_clicked
        context_menu_clicked = False    
        context_item = check_click(context_menu, x, y)
        if context_item:
            context_item['func'](item)
    elif item:
        item['func']()
            
def check_click(menu_items, x_offset=0, y_offset=0):
        for item in menu_items:
            if mouse_over(x_offset, y_offset, item):
                # print(item['name'])
                return item
        else:
            return None
        
def mouse_over(x, y, e):
    return (x + e['x'] < mouseX < x + e['x'] + textWidth(e['name']) and
            y + e['y'] < mouseY < y + e['y'] + 20)
