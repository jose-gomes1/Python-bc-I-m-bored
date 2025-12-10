import pygame
from config import BLACK

class CameraSystem:
    def __init__(self):
        # 6 rooms
        self.rooms = [pygame.Rect(200,150,500,300) for _ in range(6)]

    def draw_room(self, screen, index):
        pygame.draw.rect(screen, BLACK, self.rooms[index])
