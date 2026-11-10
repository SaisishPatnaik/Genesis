import math
import pygame
from OpenGL.GLU import gluLookAt


class Camera:
    def __init__(self):
        self.rotation_x = 48.0
        self.rotation_y = 0.0
        self.distance = 25.0
        self.min_distance = 12.0
        self.max_distance = 48.0
        self.dragging = False
        self.last_mouse = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.last_mouse = event.pos
            elif event.button == 4:
                self.distance = max(self.min_distance, self.distance - 1.5)
            elif event.button == 5:
                self.distance = min(self.max_distance, self.distance + 1.5)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            self.last_mouse = None

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            lx, ly = self.last_mouse
            self.rotation_y += (mx - lx) * 0.45
            self.rotation_x = max(12.0, min(82.0, self.rotation_x + (my - ly) * 0.35))
            self.last_mouse = event.pos

    def reset(self):
        self.__init__()

    def apply(self):
        rx = math.radians(self.rotation_x)
        ry = math.radians(self.rotation_y)
        x = self.distance * math.sin(ry) * math.cos(rx)
        y = self.distance * math.sin(rx)
        z = self.distance * math.cos(ry) * math.cos(rx)
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
