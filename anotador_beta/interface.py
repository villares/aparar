# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pranchas import Prancha
from areas import Area
from termos import criar_categorias, criar_tags
from arquivos import imagens, carrega_pranchas, salva_sessao, carrega_sessao, salva_png
from planilhas import gera_csv, gera_csv2

# offset da área que mostra a imagem da prancha
OX, OY = 200, 40
rodape = 100

MIN_SIZE = 20  # tamanho mínimo de uma área em pixels
exportar_tudo = False
imagem_prancha_atual = None

MENU_OX = 20
MENU_OY = 10
MENU_V_SPACE = 30
MENU_H_SPACE = 200
MENU_TEXT_SIZE = 18
MENU_SELECT_W = 175
MENU_SELECT_H = 20

AREA_FONT_SIZE = 18
TERM_FONT_SIZE = 14

# menu "ARQUIVO"
LOAD_PRANCHAS = "i", "carregar [i]magens"
SALVA_SESSAO = "s", "[s]alvar sessão"
LOAD_SESSAO = "c", "[c]arregar sessão"
GERA_CSV = "g", "[g]erar CSV"
SALVA_PNG = "p", "salvar [p]ng/t[o]das"
SALVA_TODAS_PNG = "o", "salvar todas png" # sem botão
EDITA_CATS = ";", "editar categorias" # sem botão
EDITA_TAGS = ":", "editar tags" # sem botão

# menu "alto da prancha"
VOLTA_PRANCHA = LEFT, "[←] volta prancha"
PROX_PRANCHA = RIGHT, "[→] prox. prancha"
ROT_PRANCHA = "9", "[9] girar imagem 90°"
ZOOM = "z", "[z] abrir imagem original"  

# menu de modos / estados de operação da ferramenta
CRIAR = "a", "[a]dicionar áreas"
EDITA = "e", "[e]ditar áreas"
ED100 = "t", "edi[t]ar 100%"
DIAGR = "d", "mostra [d]iagrama"
modos = (EDITA, ED100, CRIAR, DIAGR)
modo_ativo = CRIAR

def setup_interface():
    global botoes, comandos, categorias, tags, super_cats, imagem_prancha_atual
    Prancha.path_sessao = Prancha.path_sessao or sketchPath('data')
    Prancha.screen_height = height - (OY + rodape)
    categorias, super_cats = criar_categorias()
    tags = criar_tags()
        
    botoes = {
        ("", "ARQUIVOS"): (MENU_OX, OY,                    MENU_SELECT_W, MENU_SELECT_H),
        LOAD_PRANCHAS:    (MENU_OX, OY + MENU_V_SPACE    , MENU_SELECT_W, MENU_SELECT_H),
        SALVA_SESSAO:     (MENU_OX, OY + MENU_V_SPACE * 2, MENU_SELECT_W, MENU_SELECT_H),
        LOAD_SESSAO:      (MENU_OX, OY + MENU_V_SPACE * 3, MENU_SELECT_W, MENU_SELECT_H),
        GERA_CSV:         (MENU_OX, OY + MENU_V_SPACE * 4, MENU_SELECT_W, MENU_SELECT_H),
        SALVA_PNG:        (MENU_OX, OY + MENU_V_SPACE * 5, MENU_SELECT_W, MENU_SELECT_H),
        # modos / estados de operação da ferramenta
        ("", "ÁREAS"):    (MENU_OX, OY + MENU_V_SPACE * 7, MENU_SELECT_W, MENU_SELECT_H),
        CRIAR:            (MENU_OX, OY + MENU_V_SPACE * 8, MENU_SELECT_W, MENU_SELECT_H),
        EDITA:            (MENU_OX, OY + MENU_V_SPACE * 9, MENU_SELECT_W, MENU_SELECT_H),
        ED100:            (MENU_OX, OY + MENU_V_SPACE * 10, MENU_SELECT_W, MENU_SELECT_H),
        DIAGR:            (MENU_OX, OY + MENU_V_SPACE * 11, MENU_SELECT_W, MENU_SELECT_H),
        # menu superior ("menu da prancha")
        VOLTA_PRANCHA: (OX,                    MENU_OY, MENU_SELECT_W, MENU_SELECT_H),
        PROX_PRANCHA:  (OX + MENU_H_SPACE,     MENU_OY, MENU_SELECT_W, MENU_SELECT_H),
        ROT_PRANCHA:   (OX + MENU_H_SPACE * 2, MENU_OY, MENU_SELECT_W, MENU_SELECT_H),
        ZOOM:          (OX + MENU_H_SPACE * 3, MENU_OY, MENU_SELECT_W, MENU_SELECT_H)
    }
    # dict de funções acionadas pelos botões ou pelo teclado
    comandos = {LOAD_PRANCHAS: carrega_pranchas,
                SALVA_SESSAO: ask_salva_sessao,
                LOAD_SESSAO: ask_carrega_sessao,
                GERA_CSV: gera_planilhas,
                SALVA_PNG: salva_png,
                SALVA_TODAS_PNG: salva_todas_png,
                PROX_PRANCHA: prox_prancha,
                VOLTA_PRANCHA: volta_prancha,
                ROT_PRANCHA: rot_prancha,
                ZOOM: abre_imagem_prancha_atual, 
                EDITA_CATS: edita_categorias,
                EDITA_TAGS: edita_tags,
                }
    # imagem da prancha "exemplo" ou "home"
    splash_img_file = 'splash_img.jpg'  # aquivo na pasta /data/
    imagem_prancha_atual = img = loadImage(splash_img_file)
    fator = Prancha.calc_fator(img)
    imagens["000"] = splash_img_file
    p = Prancha("000")
    Prancha.path = sketchPath('data')
    p.areas.append(Area(OX, OY, img.width * fator, img.height * fator))
    Prancha.pranchas.append(p)

def ask_carrega_sessao():
    r = yes_no_pane("Atenção!", "Quer carregar o último estado salvo desta sessão?\n(descarta dados atuais não salvos)")
    if r == 0:
        carrega_sessao()

def ask_salva_sessao():
    r = yes_no_pane("Atenção!", "Quer salvar o estado da sessão atual?")
    if r == 0:
        salva_sessao()

def gera_planilhas():
    gera_csv()
    gera_csv2()

def edita_categorias():
    nomes = '\n'.join(categorias.keys())
    resultado = multiline_pane(title=EDITA_CATS[1], default=nomes)
    recria_categorias(resultado.split('\n'))
      
def edita_tags():
    nomes = '\n'.join(tags.keys())
    resultado = multiline_pane(title=EDITA_TAGS[1], default=nomes)
    recria_tags(resultado.split('\n'))

def recria_categorias(novos_nomes=None):
    global categorias
    novos_nomes = novos_nomes or categorias.keys()
    categorias, _ = criar_categorias(novos_nomes)

def recria_tags(novos_nomes=None):
    global tags
    novos_nomes = novos_nomes or tags.keys()
    tags = criar_tags(novos_nomes)

def salva_todas_png():
    """
    Exporta em PNG todoas as pranhcas anotadas.
    Em modo 'normal' ou em modo diagrama
    """
    global imagem_prancha_atual, exportar_tudo
    if len(Prancha.pranchas) > 1:
        Prancha.desselect_all_in_all()
        Prancha.i_atual = 1
        imagem_prancha_atual = Prancha.load_img_prancha_atual(imagens) 
        exportar_tudo = True
    else:
        Prancha.avisos("Não há pranchas para exportar.")

def prox_prancha():
    global imagem_prancha_atual
    Prancha.i_atual = (Prancha.i_atual + 1) % len(Prancha.pranchas)
    imagem_prancha_atual = Prancha.load_img_prancha_atual(imagens)

def volta_prancha():
    global imagem_prancha_atual
    Prancha.i_atual = (Prancha.i_atual - 1) % len(Prancha.pranchas)
    imagem_prancha_atual = Prancha.load_img_prancha_atual(imagens)
    
def rot_prancha():
    pa = Prancha.pranchas[Prancha.i_atual]
    pa.rot = (pa.rot + 1) % 4
    img, rot, fator = Prancha.imagem_rot_fator_atual()
    if img and (rot == 1 or rot == 3):
        pa.areas[0] = Area(OX, OY, img.height * fator, img.width * fator) # INVERTIDA
    elif img:
        pa.areas[0] = Area(OX, OY, img.width * fator, img.height * fator)

def abre_imagem_prancha_atual():
    """ comando Z: abre imagem original da prancha pelo sistema operacional ('launch()')"""
    nome_prancha_lower = Prancha.nome_prancha_atual().lower()
    if nome_prancha_lower != '000':
        path_img = imagens.get(nome_prancha_lower)
        # print(path_img)
        if path_img:        
            launch(path_img)
    else:
        Prancha.avisos("Só para pranchas de verdade!")

def mouse_over(b):
    x, y, w, h = botoes[b]
    return x < mouseX < x + w and y < mouseY < y + h

def display_botoes(DEBUG=False):
    pushStyle()
    textSize(MENU_TEXT_SIZE)
    textAlign(LEFT, TOP)    
    for b in botoes:
        tecla, nome = b
        if b == modo_ativo:
            fill(0, 0, 200)
        else:
            if mouse_over(b) and tecla != "":
                fill(255)
            else:
                fill(0)
        # desenha botão (texto)
        x, y, w, h = botoes[b]
        if DEBUG:
            pushStyle()
            noFill()
            rect(x, y, w, h)  # área clicável do texto dos botoes
            popStyle()
        text(nome, x, y)
    # Nome da prancha atual
    Prancha.display_nome_atual(OX + 4.5 * MENU_H_SPACE, MENU_OY)
    pushStyle()

def key_pressed(k, kc):
    global modo_ativo
    if k == CODED:
        k = kc

    if k in (DELETE, BACKSPACE):
       areas = Prancha.get_areas_atual()
       for a in areas[1:]: # pula a primeira área (100%) que não pode ser removida
         if a.selected:
            areas.remove(a) 
            break

    for comando in comandos.keys():
        tecla, nome = comando
        if k in (tecla, str(tecla).upper()):
            comandos[comando]()

    for modo in modos:    
        tecla, nome = modo   
        if k in (tecla, str(tecla).upper()):
            modo_ativo = modo

def mouse_pressed(mb):
    # tratamento dos botões
    global modo_ativo
    for botao in botoes:
        if mouse_over(botao):
            if botao in modos:
                modo_ativo = botao
            if botao in comandos:
                comandos[botao]()
            return  # evita que qualquer outra ação seja realizada

    areas = Prancha.get_areas_atual()
    # tratamento dos tags e categorias
    if modo_ativo in (EDITA, CRIAR):
        for a in areas:
            if a.selected:
                a.cat_and_tag_selection()
    # tratamento dos objetos Area
    if modo_ativo == EDITA:  # editar
        for a in reversed(areas):
            if a.mouse_over():
                Prancha.desselect_all()
                a.selected = True
                break
    elif modo_ativo == CRIAR and mb == LEFT:  # criar
        if areas[0].mouse_over():
            Prancha.desselect_all()
            a = Area(mouseX, mouseY, MIN_SIZE, MIN_SIZE)
            a.selected = True
            areas.append(a)

def mouse_dragged(mb):
    areas = Prancha.get_areas_atual()
    dx, dy = mouseX - pmouseX, mouseY - pmouseY
    a0 = areas[0]  # A primeira área, que o limite útil da prancha, referência de 100%
    if modo_ativo == ED100:
        if mb == LEFT:
            x = a0.x + dx
            y = a0.y + dy
            na_tela = 0 < x < width - a0.w and 0 < y < height - a0.h
            if na_tela:
                a0.x = x
                a0.y = y
        else:
            if a0.w + dx > MIN_SIZE:
                a0.w += dx
            if a0.h + dy > MIN_SIZE:
                a0.h += dy
    for r in reversed(areas[1:]):
        # pula a primeira área (100%) que não pode ser editada nestes modos que seguem
        if r.selected:
            if modo_ativo == EDITA and mb == LEFT:
                x = r.x + dx
                y = r.y + dy
                na_tela = 0 < x < width - r.w and 0 < y < height - r.h
                if na_tela:
                    r.x = x
                    r.y = y
            elif modo_ativo in (EDITA, CRIAR) and mb == RIGHT:
                if r.w + dx > MIN_SIZE:
                    r.w = r.w + dx
                if r.h + dy > MIN_SIZE:
                    r.h = r.h + dy
            elif modo_ativo == CRIAR and areas[0].mouse_over():
                if mouseX - r.x > MIN_SIZE:
                    r.w = mouseX - r.x
                if mouseY - r.y > MIN_SIZE:
                    r.h = mouseY - r.y

def mouse_wheel(e):
    areas = Prancha.get_areas_atual()
    if modo_ativo in (EDITA, CRIAR):   # editar ou criar
        for a in reversed(areas[1:]):  # pula a primeira área (100%) que não pode ser girada
            if a.mouse_over():
                a.rotation += radians(e.getCount())
                break
    
def yes_no_pane(title, message):
    # Sim é 0, Não é 1, fechar a janela é -1
    from javax.swing import JOptionPane
    return JOptionPane.showConfirmDialog(None,
                                         message,
                                         title,
                                         JOptionPane.YES_NO_OPTION)
    
def multiline_pane(title='', default=''):
    from javax.swing import JOptionPane, JScrollPane, JTextArea
    ta = JTextArea(20, 20)
    ta.setText(default)
    result = JOptionPane.showConfirmDialog(None,
                                           JScrollPane(ta),
                                           title,
                                           JOptionPane.OK_CANCEL_OPTION,
                                           JOptionPane.PLAIN_MESSAGE,
                                           # JOptionPane.QUESTION_MESSAGE
                                           )
    if result == JOptionPane.OK_OPTION:
        return ta.getText()
    else: 
        return default
    
def option_pane(title, message, options, default=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(
        None,
        message,
        title,
        JOptionPane.QUESTION_MESSAGE,
        None,
        options,
        default)  # must be in options, otherwise 1st is shown
    
def input_pane(question='', suggestion=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(None, question, suggestion)
