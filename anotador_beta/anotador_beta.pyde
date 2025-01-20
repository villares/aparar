"""
APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
github.com/villares/aparar

Uma feramenta experimental do grupo de pesquisa do Prof. Dr. Daniel de Carvalho Moreira
Colaboradores: Carolina Celete, Raissa Rodrigues, Larissa Negris de Souza e Alexandre Villares

Embrião do código de retângulos reconfiguráveis aproveitado do projeto
co-criar co-mover de Graziele Lautenschlaeger https://github.com/grazilaut/co_criar_co_mover

---

APARAR - Anotador de Pranchas para Análise e Registro de Áreas Relativas
Copyright (C) 2025 Alexandre B A Villares
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
    # Mostra imagem da prancha (se não estiver no modo digagrama)
    if interface.modo_ativo != interface.DIAGR:
        Prancha.display_imagem_atual(imagens)
    # Desenha as áreas anotadas        
    Prancha.display_areas_atual(mousePressed, DEBUG)
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
    global DEBUG
    if key == '!': DEBUG = not DEBUG
    
def mouseWheel(e):
    interface.mouse_wheel(e)    
    
def stop():
    r = interface.yes_no_pane("Fechando a ferramenta!", "Quer salvar a sessão?")
    if r == 0:
        salva_sessao()
