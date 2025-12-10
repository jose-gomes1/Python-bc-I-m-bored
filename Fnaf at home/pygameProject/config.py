import pygame

WIDTH, HEIGHT = 1024, 600
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (120,120,120)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BROWN = (139,69,19)
FOX_RED = (200,0,0)
GOLD = (255,215,0)

ANIMATRONIC_EVENT = pygame.USEREVENT + 1

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 22)
