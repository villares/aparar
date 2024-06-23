# PY5 IMPORTED MODE CODE

import pickle
from pathlib import Path

import pranchas as pr
from areas import Area
import interface

imagens = {}  # dicionário contendo os caminhos para carregar as imagens das pranchas

NOME_ARQ_SESSAO = "sessao_aparar_v20210305.pickle"
NOME_ARQ_SESSAO_LEGADO = "sessao_aparar_v20210104ire.pickle"

def lista_imagens(dir=None):
    """
    Devolve uma a lista de caminhos completos (paths) dos arquivos de imagem
    para cada imagem na pasta `dir` ou na pasta /data/ do diretório corrente
    """
    def has_image_ext(file_path):
        # extensões dos formatos de imagem aceitos
        valid_ext = ('.jpg', '.png', '.jpeg', '.gif', '.tif', '.tga')
        return file_path.suffix.lower() in valid_ext

    data_path = dir or Path.cwd() / 'data'
    try:
        p_list = [fp for fp in Path(dir).iterdir()
                  if fp.is_file() and has_image_ext(fp)]
    except Exception as e:
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
        return []
    return p_list

def carrega_pranchas():
    # Operação normal de adicionar_imagens() é via callback disparado por selectFolder()
    select_folder("Selecione uma pasta", adicionar_imagens)
    # Para o debug, talvez seja preciso comentar a linha acima e
    # usar "chamada direta" de adicionar_imagens() abaixo
    # adicionar_imagens(Path("/home/villares/Área de Trabalho/APARAR/pr.Pranchas para teste"))

def adicionar_imagens(selection):
    if selection == None:
        pr.Prancha.avisos("Seleção da pasta cancelada")
    else:
        pr.Prancha.path_sessao = selection
        pr.Prancha.nome_sessao = selection.name
        print("Pasta selecionada: " + str(selection))
        # ESTA PARTE FINAL MUDA NA VERSAO QUE NAO MANTEM IMAGENS NA MEMORIA
        caminhos_imagens = lista_imagens(selection)
        for image_path in caminhos_imagens:
            imagens[image_path.name.lower()] = image_path
        if not carrega_sessao() or (len(imagens) != len(pr.Prancha.pranchas) - 1):
            for image_path in caminhos_imagens:
                pr.Prancha.avisos("carregando imagens")
                img = load_image(image_path)
                imagens[image_path.name.lower()] = image_path
                fator = pr.Prancha.calc_fator(img)
                if not pr.Prancha.in_pranchas(img_name):
                    p = pr.Prancha(img_name)
                    p.areas.append(Area(interface.OX, interface.OY,
                                        img.width * fator, img.height * fator))
                    pr.Prancha.pranchas.append(p)

def salva_sessao():
    with open(pr.Prancha.path_sessao / NOME_ARQ_SESSAO, "wb") as file:
        # Cats e tags entraram no antigo slot de pr.Prancha.path_sessao no Pickle!
        sessao = (pr.Prancha.pranchas, (interface.categorias, interface.tags), pr.Prancha.screen_height)
        pickle.dump(sessao, file)
    mensagem = "sessão salva em …" + unicode(pr.Prancha.path_sessao)[-40:]
    pr.Prancha.avisos(mensagem)
    print(mensagem)

def carrega_sessao():
    if (pr.Prancha.path_sessao / NOME_ARQ_SESSAO).is_file():
        PATH_ARQ_SESSAO =pr.Prancha.path_sessao / NOME_ARQ_SESSAO
    else:
        PATH_ARQ_SESSAO = pr.Prancha.path_sessao / NOME_ARQ_SESSAO_LEGADO        
    try:
        with open(PATH_ARQ_SESSAO, "rb") as file:
            pr.Prancha.pranchas, cats_e_tags, pr.Prancha.screen_height = pickle.load(file)
            pr.Prancha.update_for_screen_change()
            pr.Prancha.update_for_name_change()
            if cats_e_tags != pr.Prancha.path_sessao and len(cats_e_tags) == 2: 
                # compatibilidade com arquivos antigos!
                interface.categorias, interface.tags = cats_e_tags
                print("Categorias e tags carregados da sessão salva!")
            mensagem = "Sessao carregada de …" + str(PATH_ARQ_SESSAO)[-40:]
            pr.Prancha.avisos(mensagem)
            print(mensagem)
            return True
    except Exception as e:
        # pode ser que não havia sessão ou outro erro...
        pr.Prancha.avisos("não foi carregada uma sessão salva")
        print("Deve imprimir 'Erro (File IO)', senão tem algo errado!")
        print("Erro ({})".format(e))
        return False

def salva_png():
    """
    Inicialmente salva apenas imagem da "pr.Prancha atual",
    no modo normal de edição ou modo diagrama.
    """
    modo_diagrama = interface.modo_ativo == interface.DIAGR
    prefixo = "diagrama" if modo_diagrama else "imagem"
    nome_arquivo = "{}-{}.png".format(prefixo, pr.Prancha.nome_prancha_atual())
    sub_folder = "diagramas" if modo_diagrama else "imagens"
    path_folder = pr.Prancha.path_sessao / sub_folder  # pasta diagramas ou imagens
    path_arquivo = path_folder / nome_arquivo
    area = pr.Prancha.get_areas_atual()[0]
    x, y = int(area.x), int(area.y)
    w, h = int(area.w), int(area.h)
    # Para salvar só a área 100% da prancha
    # Salva img temporária da tela toda, não queria ter que usar isso :(
    tem_path = Path.cwd() / 'data' / 'temp.png'
    save_frame(tem_path)
    temp = load_image(tem_path)
    png = create_graphics(w, h)
    png.begin_draw()
    png.background(255)
    png.copy(temp, x + 1, y + 1, w, h, 0, 0, w, h)
    png.save(path_arquivo)  # salva arquivo só com o conteúdo da área do 100%
    png.end_draw()
    if modo_diagrama:
        salva_legenda_diagrama(path)
    pr.Prancha.avisos("Imagem salva: {}".format(nome_arquivo))

def salva_legenda_diagrama(path):
    png = create_graphics(300, 700)
    png.begin_draw()
    png.background(200)
    nomes_categorias = sorted(interface.categorias.keys())
    for i, nome_cat in enumerate(nomes_categorias):
        png.fill(Area.calc_color(nome_cat))
        png.rect(20, i * 25, 40, 20)
        png.fill(0)
        png.text(nome_cat, 70, 15 + i * 25)
    png.save(Path(path) / "legenda.png")
    png.end_draw()
