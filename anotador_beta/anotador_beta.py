"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover
"""

# [WIP] Modo diagrama
#     [ ] Patterns PB para legenda de categorias
# [ ] Opção de aumentar o rodapé para corrigir problema de pranchas longas!
# [ ] Conferir operação em telas menores com 1024 px de largura (talvez reduzir texto).
# [WIP] Editar tags e categorias ("termos")
# ****[ ] Areas com uma categoria/tags que foram removidos quebram a exportação de planiha!!! ****
#     [X] Sessão agora salva tags e categorias
#     [/] Interface com janela para editar nomes (já permite acrescentar termos)
#     [ ] Renomear termo (procurar aplicações do termo nas Areas)
#     [ ] Remover termo (remover aplicações)

import interface
import pranchas
from arquivos import imagens, adicionar_imagens, salva_sessao, salva_png

DEBUG = False

def setup():
    size(1500, 740)
    #full_screen()
    interface.setup_interface()

def draw():
    background(200)
    # Elementos de interface/menu
    interface.display_botoes(DEBUG)
    # Mostra imagem da prancha (se não estiver no modo digagrama)
    if interface.modo_ativo != interface.DIAGR:
        pranchas.Prancha.display_imagem_atual(imagens)
    # Desenha as áreas anotadas        
    pranchas.Prancha.display_areas_atual(is_mouse_pressed, DEBUG)
    # Tratamento do flag de exportar todas as pranchas
    if interface.exportar_tudo:   
        salva_png()
        interface.prox_prancha()  # next from last is 0
        if pranchas.Prancha.i_atual == 0:  # it will not be exported
            interface.exportar_tudo = False
    # Textos de aviso
    pranchas.Prancha.avisos()

def mouse_pressed():
    interface.mouse_pressed(mouse_button)

def mouse_dragged():
    interface.mouse_dragged(mouse_button)

def key_pressed():
    interface.key_pressed(key, key_code)
    global DEBUG
    if key == '!': DEBUG = not DEBUG
    
def mouse_wheel(e):
    interface.mouse_wheel(e)    
    
def stop():
    r = interface.yes_no_pane("Fechando a ferramenta!", "Quer salvar a sessão?")
    if r == 0:
        salva_sessao()
