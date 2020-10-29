# -*- coding: utf-8 -*-

class Area:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.selected = False
        self.over = False
        self.area = self.w * self.h
        self.cobertura = 1

    def display(self, mp):
        stroke(0)
        if self.selected:
            stroke(200, 0, 0)
            strokeWeight(3)
        elif self.over and not mp:
            strokeWeight(5)
            self.over = False
        else:
            strokeWeight(2)
        fill(0, 20)
        rect(self.x, self.y, self.w, self.h)
        fill(0)
        text('{:2.0%}'.format(self.cobertura), self.x, self.y + 20)

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w
            and self.y < mouseY < self.y + self.h)
