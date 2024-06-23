# PY5 IMPORTED MODE CODE

from termos import setup_terms_state, active_term_state, draw_terms, select_cat, select_tag
import pranchas # para usar nome_prancha_atual()
import interface

class Area:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.selected = False
        self.over = False
        self.area = self.w * self.h
        self.cobertura = 1  # 100%
        self.tags_state = setup_terms_state(Area.tags)  # *
        self.categorias_state = setup_terms_state(Area.categorias)  # *
        self.cat_selected = ""
        self.scat_selected = None
        self.tags_selected = []
        self.rotation = 0

    def update(self):
        # atualiza qual categoria desta área
        self.cat_selected = active_term_state(self.categorias_state)
        # atualiza, se tiver, supercategoria (categoria-prefixo)
        sep_pos = self.cat_selected.find("-")
        if sep_pos > 0:
            self.scat_selected = self.cat_selected[:sep_pos]
        else:
            self.scat_selected = None
        # atualiza lista de tags que estão selecionados
        self.tags_selected = active_term_state(self.tags_state, all=True)

    def display(self, mp, DEBUG=False):
        self.update()
        modo_anotativo = (interface.modo_ativo == interface.EDITA or
                          interface.modo_ativo == interface.CRIAR)
        modo_diagrama = interface.modo_ativo == interface.DIAGR
        push_style()
        text_size(interface.TERM_FONT_SIZE)
        stroke(0)
        if self.selected and self.cobertura != 1 and not modo_diagrama:
            stroke(200, 0, 0)
            strokeWeight(3)
            if modo_anotativo:
                draw_terms(Area.categorias, self.categorias_state, DEBUG)
                draw_terms(Area.tags, self.tags_state, DEBUG)
        elif self.over and self.cobertura != 1 and not modo_diagrama:
            stroke_weight(5)
            self.over = False
        else:
            stroke_weight(2)
        # pega dados da categoria que está selecionada (se houver)
        cat = Area.categorias.get(self.cat_selected)
        if cat and modo_diagrama:
            fill(Area.calc_color(self.cat_selected))
            no_stroke()
        else:  # senão usa cinza translúcido padrão
            fill(0, 20)
        # caso especial do modo de editar área de referência 100%
        if interface.modo_ativo == interface.ED100:
            if self.cobertura == 1:
                stroke(200, 0, 0)
                stroke_weight(5)
            else:
                stroke(0)
                stroke_weight(3)
        # desenha o retângulo da área
        push()
        translate(self.x + self.w / 2, self.y + self.h / 2)
        rotate(self.rotation)
        rect(-self.w / 2, -self.h / 2, self.w, self.h)
        pop()
        fill(0)  # textos da área em preto
        if not modo_diagrama:
            text_align(LEFT, TOP)
            text(self.cat_selected,
                 self.x + 10,
                 self.y + 10)
        text_align(CENTER, CENTER)
        text_size(interface.AREA_FONT_SIZE)
        # caso da área de referência 100% (cobertura == 1)
        if self.cobertura == 1 and modo_diagrama:
            text(pranchas.Prancha.nome_prancha_atual(),
                 self.x + self.w / 2,
                 self.y + self.h - 20)
        else:
            text("{:2.1%}".format(self.cobertura),
                 self.x + self.w / 2,
                 self.y + self.h - 20)
        pop_style()

    def cat_and_tag_selection(self):
        if self.cobertura != 1:  # menos para a àrea de ref. 100%
            select_cat(Area.categorias, self.categorias_state)
            select_tag(Area.tags, self.tags_state)

    def mouse_over(self):
        rp = rect_points(self.x + self.w / 2,
                         self.y + self.h / 2,
                         self.w, self.h,
                         mode=CENTER,
                         angle=self.rotation
                         )
        return point_inside_poly(mouse_x, mouse_y, rp)

    @staticmethod
    def calc_color(cat_name):
        cat = Area.categorias.get(cat_name)
        if cat:
            h = cat['id_cor']
            with push():
                color_mode(HSB)
                return color(h, 128 + 128 * (h % 2), 255 - 128 * (h % 3), 155)

def point_inside_poly(x, y, pts):
    # ray-casting algorithm based on
    # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
    inside = False
    for i, p in enumerate(pts):
        pp = pts[i - 1]
        xi, yi = p
        xj, yj = pp
        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            inside = not inside
    return inside

def rect_points(ox, oy, w, h, mode=CORNER, angle=None):
    if mode == CENTER:
        x, y = ox - w / 2.0, oy - h / 2.0
    else:
        x, y = ox, oy
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if angle is None:
        return pts
    else:
        return [rotate_point((x, y), angle, (ox, oy))
                for x, y in pts]

def rotate_point(*args):
    (xp, yp), angle, (x0, y0) = args
    x, y = xp - x0, yp - y0  # translate to origin
    xr = x * cos(angle) - y * sin(angle)
    yr = y * cos(angle) + x * sin(angle)
    return (xr + x0, yr + y0)
