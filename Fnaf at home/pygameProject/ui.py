import pygame
from config import WHITE

class UI:
    def __init__(self):
        # Doors
        self.left_button = pygame.Rect(50, 400, 120, 50)
        self.right_button = pygame.Rect(730, 400, 120, 50)
        # Cameras / back button
        self.camera_office_button = pygame.Rect(20, 20, 120, 40)  # top-left
        # Camera selection buttons at bottom
        self.camera_buttons = [
            pygame.Rect(150 + 120*i, 500, 100, 50) for i in range(6)
        ]

    def draw_button(self, screen, rect, text, active=False):
        color = (0,200,0) if active else (100,100,100)
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.SysFont("Arial", 20)
        label = font.render(text, True, WHITE)
        screen.blit(label, (rect.x + 5, rect.y + 5))

    def draw(self, screen, player, message):
        self.draw_button(screen, self.left_button, "LEFT DOOR", active=player.left_door_closed)
        self.draw_button(screen, self.right_button, "RIGHT DOOR", active=player.right_door_closed)
        self.draw_button(screen, self.camera_office_button, "CAMERAS", active=player.in_cameras)
        for i, btn in enumerate(self.camera_buttons):
            self.draw_button(screen, btn, f"CAM {i+1}", active=(player.camera_index==i+1))
        if message:
            font = pygame.font.SysFont("Arial", 24)
            label = font.render(message, True, WHITE)
            screen.blit(label, (20, 70))
