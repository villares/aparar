"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""

# [WIP] RETÂNGULOS GIRADOS
# [WIP] Modo diagrama
#   [X] SALVAR DIAGRAMA COM ÁREA TRANSLÚCIDA
#   [X] salvar legenda cores -> categorias
#   [ ] patterns PB para legenda de categorias
#   [ ] salvar diagrama de todas as pranchas...
# [X] CSV especial com tags por categoria
# [X] Travar ediçao do 100%
# [X] NÃO CARREGA IMAGENS TODAS NA MEMORIA
# [WIP] Separar estado das categorias/tags (terms_state) dos botões (terms) de forma a reduzir consumo de memória
# [-] Modo ZOOM - não sei se vou fazer
# [X] Melhor suporte a fullScreen() 
# [ ] opção de aumentar o rodapé para corrigir problema de pranchas longas!
# [X] Não salva sessão, depois de carregar imagens, muda aviso de imagens carregando, arruma epxort PNG

from __future__ import unicode_literals

import interface
from areas import Area
from pranchas import Prancha
from arquivos import imagens, adicionar_imagens, salva_sessao

DEBUG = False

def setup():
    # size(1200, 740)
    fullScreen()
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
    
def mouseWheel(e):
    interface.mouse_wheel(e)    
    
def stop():
    r = interface.yes_no_pane("Fechando a ferramenta!", "Quer salvar a sessão?")
    if r == 0:
        salva_sessao()
