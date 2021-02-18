"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""

# [WIP] Modo diagrama
#     [ ] patterns PB para legenda de categorias
# [ ] opção de aumentar o rodapé para corrigir problema de pranchas longas!
# [X] Aredondamento das áreas com 1 casa decimal: 0.5%  3.6% etc...
# [X] Aceita códigos longos par IDs dos nomes de arquivo! AA...A_BB...B_CCC  
#     o último campo vai ser truncado nos 3 caracteres iniciais  ..._CCCCXXXXX -> CCC
# [X] Desselecionar todas as àreas em caso de exportação de todas as imagens ou diagramas 
#     (Na exportação de um único PNG você continua precisando tirar manualmente a seleção)
# [EXPERIMENTAL] tecla 'z' abre a imagem original da prancha (para dar zoom!)

from __future__ import unicode_literals

import interface
from areas import Area
from pranchas import Prancha
from arquivos import imagens, adicionar_imagens, salva_sessao, salva_png

DEBUG = False

def setup():
    # size(1200, 740)
    fullScreen()
    interface.setup_interface()

def draw():
    background(200)
    # Elementos de interface/menu
    interface.display_botoes(DEBUG)
    # Nome da prancha atual
    Prancha.display_nome_atual()
    # Mostra imagem da prancha (se não estiver no modo digagrama)
    if interface.modo_ativo != interface.DIAGR:
        Prancha.display_imagem_atual(imagens)
    # Desenha as áreas anotadas        
    Prancha.display_areas_atual(mousePressed)
    # Tratamento do flag de exportar todas as pranchas
    if interface.exportar_tudo:   
        salva_png()
        interface.prox_prancha()  # next from last is 0
        if Prancha.i_atual == 0:  # it will not be exported
            interface.exportar_tudo = False
    # Textos de aviso
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
