# -*- coding: utf-8 -*-

class Area:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.drag = False
        self.destaque = False
        self.area = self.w * self.h

    def display(self, mp):
        colorMode(HSB)
        noFill()
        area = abs(self.w * self.h)
        matiz = area * 255 / (width * height)
        stroke(matiz, 255, 255)
        colorMode(RGB)

        if self.drag:
            strokeWeight(5)

        elif self.destaque and not mp:
            stroke(0)
            strokeWeight(3)
            self.destaque = False
        else:
            strokeWeight(2)

        rect(self.x, self.y, self.w, self.h)

        self.area = self.w * self.h

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w
            and self.y < mouseY < self.y + self.h)
