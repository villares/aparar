"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""
# arquivos categorias.txt e tags.txt na pasta /data/
# [ ] Melhorar display de nomes longos de categoria...
# [ ] Salvar sessão na pasta das últimas imagens carregadas
# [ ] Evitar crash se não carregou as imagens...
# [ ] Gerar planilha CSV

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
    Prancha.display_imagem_atual(imagens)
    Prancha.display_areas_atual(mousePressed)

def mousePressed():
    interface.mouse_pressed(mouseButton)

def mouseDragged():
    interface.mouse_dragged(mouseButton)

def keyPressed():
    interface.key_pressed(key, keyCode)
