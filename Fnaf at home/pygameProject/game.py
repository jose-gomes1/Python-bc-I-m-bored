import pygame
import random
import time
from config import *
from player import Player
from ui import UI
from animatronic import BaseAnimatronic, Foxy

pygame.init()

WIDTH, HEIGHT = 900, 600
FPS = 60
FONT = pygame.font.SysFont("Arial", 24)
WHITE = (255, 255, 255)

CAM_RECTS = {i: pygame.Rect(200, 110, 500, 320) for i in range(1, 8)}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FNaF Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = UI()
        self.player = Player()

        self.hour = 12
        self.minute = 0
        self.night_timer = 0
        self.total_night_seconds = 240  # 4 minutes
        self.seconds_per_hour = self.total_night_seconds / 6 
        self.seconds_per_minute = self.seconds_per_hour / 60

        # -----------------------
        # ANIMATRONICS
        # -----------------------
        self.bonnie = BaseAnimatronic(
            "Bonnie", (120, 0, 255), [1, 2, 3, 4, 7], move_time=14.0
        )
        self.chica = BaseAnimatronic(
            "Chica", (255, 255, 0), [1, 2, 5, 6, 7], move_time=14.0
        )
        self.freddy = BaseAnimatronic(
            "Freddy", (150, 80, 20), [1, 3, 6, 7], move_time=18.0
        )

        self.foxy = Foxy()

        self.animatronics = [self.bonnie, self.chica, self.freddy]

        self.message = ""
        self.message_timer = 0

        self.last_flip_time = time.time()
        self.flip_count = 0
    
    def set_message(self, msg, time_s=2.0):
        self.message = msg
        self.message_timer = time_s

    # -----------------------
    # EVENTS
    # -----------------------
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse(*event.pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.toggle_left()
            elif event.key == pygame.K_d:
                self.player.toggle_right()
            elif event.key == pygame.K_s:
                self.player.in_cameras = not self.player.in_cameras
                self.player.camera_index = 1 if self.player.in_cameras else 7

            elif pygame.K_KP1 <= event.key <= pygame.K_KP7:
                if self.player.in_cameras:
                    self.player.camera_index = event.key - pygame.K_KP1 + 1

    def handle_mouse(self, mx, my):
        if self.ui.camera_office_button.collidepoint((mx, my)):
            self.player.in_cameras = not self.player.in_cameras
            self.player.camera_index = 1 if self.player.in_cameras else 7
            return

        if not self.player.in_cameras:
            if self.ui.left_button.collidepoint((mx, my)):
                self.player.toggle_left()
            elif self.ui.right_button.collidepoint((mx, my)):
                self.player.toggle_right()
        else:
            for i, btn in enumerate(self.ui.camera_buttons):
                if btn.collidepoint((mx, my)):
                    self.player.camera_index = i + 1
                    self.register_camera_flip()

    # -----------------------
    # CAMERA FLIPS
    # -----------------------
    def register_camera_flip(self):
        now = time.time()
        if now - self.last_flip_time > 4:
            self.flip_count = 0
        self.flip_count += 1
        self.last_flip_time = now

    # -----------------------
    # ATTACK RESOLUTION
    # -----------------------
    def resolve_attack(self, anim):
        if anim.name == "Bonnie":
            if self.player.left_door_closed:
                anim.attacking = False
            else:
                self.game_over("Bonnie")

        elif anim.name == "Chica":
            if self.player.right_door_closed:
                anim.attacking = False
            else:
                self.game_over("Chica")

        elif anim.name == "Freddy":
            # If player is watching his final camera OR left/right door is closed, he cannot attack
            if (self.player.in_cameras and self.player.camera_index == anim.path[-1]) or self.player.right_door_closed:
                anim.attacking = False
                anim.in_warning = False
            else:
                self.game_over("Freddy")


    def resolve_foxy_attack(self):
        if self.foxy.attacking:
            if self.player.left_door_closed:
                self.foxy.reset_charge()
            else:
                self.game_over("Foxy")

    # -----------------------
    # UPDATE
    # -----------------------
    def update(self, dt):
        self.night_timer += dt

        progress = min(self.night_timer / self.total_night_seconds, 1.0)

        # Convert progress to hours passed (0 → 6)
        hours_passed = int(progress * 6)

        # Display clock (12 → 1 → 2 → ... → 6)
        self.hour = 12 + hours_passed
        if self.hour > 12:
            self.hour -= 12

        # End of night
        if progress >= 1.0:
            print("6 AM — YOU WIN")
            self.running = False

        self.player.music_box = max(0, self.player.music_box - 4 * dt)
        if self.player.in_cameras and self.player.camera_index == 6:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.music_box = min(100, self.player.music_box + 35 * dt)
        if self.player.music_box <= 0:
            self.game_over("Puppet")

        # -----------------------
        # POWER
        # -----------------------
        self.player.drain_power(dt)
        if self.player.power <= 0:
            self.game_over("Power Out")

        # -----------------------
        # ANIMATRONICS
        # -----------------------
        for anim in self.animatronics:
            # Increment timer normally for all animatronics
            anim.timer += dt

            # Warning stage
            if anim.timer >= anim.move_time and not anim.in_warning:
                anim.in_warning = True
                anim.warning_time = 2.0  # time to react
                anim.timer = 0

            # Countdown warning
            if anim.in_warning:
                anim.warning_time -= dt
                if anim.warning_time <= 0:
                    anim.in_warning = False
                    anim.path_idx += 1
                    anim.timer = 0
                    if anim.path_idx >= len(anim.path) - 1:
                        anim.attacking = True

            # Freddy special: stall **only during the warning** at the final camera
            if anim.name == "Freddy":
                if self.player.in_cameras and self.player.camera_index == anim.path[-1] and anim.in_warning:
                    anim.attacking = False  # pause attack while watching
            # Trigger attacks
            if anim.attacking:
                self.resolve_attack(anim)

    # -----------------------
    # DRAW
    # -----------------------
    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.player.in_cameras:
            self.draw_camera_view()
        else:
            self.draw_office_view()

        time_lbl = FONT.render(f"{self.hour}:{self.minute:02d} AM", True, WHITE)
        self.screen.blit(time_lbl, (WIDTH - 160, 20))

        self.ui.draw(self.screen, self.player, self.message)
        pygame.display.flip()

    def draw_camera_view(self):
        cam = self.player.camera_index
        rect = CAM_RECTS[cam]
        pygame.draw.rect(self.screen, (20, 20, 20), rect)
        pygame.draw.rect(self.screen, (70, 70, 70), rect, 3)

        for anim in self.animatronics:
            if anim.path_idx < len(anim.path) and anim.path[anim.path_idx] == cam:
                pygame.draw.rect(
                    self.screen,
                    anim.color,
                    (rect.centerx - 40, rect.centery - 80, 80, 160)
                )

                if anim.in_warning:
                    lbl = FONT.render(
                        f"{anim.name} WARNING!",
                        True,
                        anim.color
                    )
                    self.screen.blit(lbl, (rect.x + 20, rect.y + 20))
        
        if cam == 6:
            rect = CAM_RECTS[6]
            bar_width, bar_height = 150, 20
            x, y = rect.x + 20, rect.y + 20
            # Background bar
            pygame.draw.rect(self.screen, (50,50,50), (x, y, bar_width, bar_height))
            # Filled portion
            fill_width = int(bar_width * (self.player.music_box / 100))
            pygame.draw.rect(self.screen, (0,255,0), (x, y, fill_width, bar_height))
            # Label
            lbl = FONT.render("Music Box", True, (255,255,255))
            self.screen.blit(lbl, (x, y-20))

        if cam == 2:
            fx = pygame.Rect(rect.centerx - 40, rect.centery - 80, 80, 160)

            color = (
                min(255, 80 + self.foxy.stage * 60),
                50,
                50
            )

            pygame.draw.rect(self.screen, color, fx)

            lbl = FONT.render(f"Foxy stage {self.foxy.stage}/3", True, WHITE)
            self.screen.blit(lbl, (rect.x + 20, rect.y + 20))

            if self.foxy.running:
                warn = FONT.render("FOXY RUNNING!", True, color)
                self.screen.blit(warn, (rect.x + 20, rect.y + 50))

    def draw_office_view(self):
        rect = CAM_RECTS[7]
        pygame.draw.rect(self.screen, (10, 10, 15), rect)
        pygame.draw.rect(self.screen, (60, 60, 60), rect, 3)

    # -----------------------
    # GAME OVER
    # -----------------------
    def game_over(self, who):
        print(f"{who} got you!")
        self.running = False

    # -----------------------
    # MAIN LOOP
    # -----------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                self.handle_event(event)

            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    Game().run()
