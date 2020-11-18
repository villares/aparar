"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""
# [WIP] Modo diagrama
#   [X] salvar diagrama de uma prancha
#   [X] salvara só a àrea da prancha
#   [X] SALVAR DIAGRAMA COM ÁREA TRANSLÚCIDA
#   [ ] salvar legenda cores -> categorias
#   [ ] salvar diagrama de todas as pranchas...
# [ ] CSV especial com tags por categoria
# [X] Travar ediçao do 100%
# [B] NÃO CARREGA IMAGENS TODAS NA MEMORIA - tá num branch
# [WIP] Separar estado das categorias/tags (terms_state) dos botões (terms) de forma a reduzir consumo de memória
# [-] Modo ZOOM - não sei se vou fazer
# [ ] Melhor suporte a fullScreen() 

from __future__ import unicode_literals

import interface
from areas import Area
from pranchas import Prancha
from arquivos import imagens, adicionar_imagens

DEBUG = False

def setup():
    size(1200, 700)
    # fullScreen()
    interface.setup_interface()

def draw():
    background(200)
    interface.display_botoes(DEBUG)
    Prancha.display_nome_atual()
    if not Prancha.DIAGRAMA:
        Prancha.display_imagem_atual(imagens)
    Prancha.display_areas_atual(mousePressed)
    Prancha.avisos()

def mousePressed():
    interface.mouse_pressed(mouseButton)

def mouseDragged():
    interface.mouse_dragged(mouseButton)

def keyPressed():
    interface.key_pressed(key, keyCode)
    print key
