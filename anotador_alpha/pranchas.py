# -*- coding: utf-8 -*-

class Prancha:
    
    atual = 0
    pranchas = []
        
    def __init__ (self, nome):
        self.areas = []
        self.nome = nome
        
    def display_areas(self, mp):
        for r in reversed(self.areas):
            if r.mouse_over():
                r.destaque = True
                break
        for r in reversed(self.areas):
            r.display(mp)
        
    def update(self):
        primeiro = areas[0]
        primeiro.cobertura = 1
        total = primeiro.area
        for r in self.areas[1:]:
            r.cobertura = r.area / total
            
    @classmethod
    def in_pranchas(cls, nome):
        return nome in cls.get_names()
        
    @classmethod        
    def get_names(cls):
        names = [p.nome for p in cls.pranchas]
            
    @classmethod
    def display_nome_atual(cls):
        fill(200, 0, 0)
        text(cls.nome_prancha_atual(), 400, 30) 
                       
    @classmethod
    def nome_prancha_atual(cls):
        return cls.pranchas[cls.atual].nome
                                          
    @classmethod
    def display_imagem_atual(cls, imagens):
        img = imagens[cls.nome_prancha_atual().lower()]
        fator = float(height - 100) / img.height
        image(img, cls.ox, cls.oy,
              img.width * fator, img.height * fator)

    @classmethod    
    def display_areas_atual(cls, mp):
        cls.pranchas[cls.atual].display_areas(mp)
           
    @classmethod
    def get_areas_atual(cls):
        return cls.pranchas[cls.atual].areas
