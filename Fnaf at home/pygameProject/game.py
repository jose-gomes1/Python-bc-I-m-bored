import pygame
import random
import time
from config import *
from player import Player
from ui import UI
from animatronic import BaseAnimatronic, Foxy, GoldenFreddy

CAM_RECTS = {i: pygame.Rect(200, 110, 500, 320) for i in range(1, 8)}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FNaF Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = UI()
        self.player = Player()

        # Night speed scaling
        BASE_NIGHT_LENGTH = 240  # base 4 minutes
        NEW_NIGHT_LENGTH = 480   # 8 minutes
        self.night_speed_factor = BASE_NIGHT_LENGTH / NEW_NIGHT_LENGTH

        # Animatronics
        self.bonnie = BaseAnimatronic("Bonnie", (120,0,255), [1,2,3,4,7], move_time=6.0)
        self.chica  = BaseAnimatronic("Chica", (255,255,0), [1,2,5,6,7], move_time=6.0)
        self.freddy = BaseAnimatronic("Freddy", (150,80,20), [1,3,6,7], move_time=7.0)
        self.foxy   = Foxy()
        self.golden = GoldenFreddy()
        self.animatronics = [self.bonnie, self.chica, self.freddy]

        # Stagger start timers
        self.bonnie.timer = random.uniform(0, self.bonnie.move_time)
        self.chica.timer  = random.uniform(0, self.chica.move_time)
        self.freddy.timer = random.uniform(0, self.freddy.move_time)

        self.message = ""
        self.message_timer = 0
        self.last_flip_time = 0
        self.flip_count = 0

        # Clock
        self.hour = 12
        self.minute = 0
        self.time_accumulator = 0
        self.total_night_seconds = 660
        self.seconds_per_hour = 100
        self.seconds_per_minute = 16

    # -----------------------
    # EVENTS
    # -----------------------
    def handle_mouse(self, mx, my):
        if self.ui.camera_office_button.collidepoint((mx, my)):
            if self.player.in_cameras:
                self.player.in_cameras = False
                self.player.camera_index = 7
                self.set_message("Returned to office", 1.0)
            else:
                self.player.in_cameras = True
                self.player.camera_index = 1
                self.set_message("Entered cameras", 1.0)
            return

        if not self.player.in_cameras:
            if self.ui.left_button.collidepoint((mx,my)):
                self.player.toggle_left()
                self.set_message("Left door toggled", 1.5)
            elif self.ui.right_button.collidepoint((mx,my)):
                self.player.toggle_right()
                self.set_message("Right door toggled", 1.5)
        else:
            for i, btn in enumerate(self.ui.camera_buttons):
                if btn.collidepoint((mx, my)):
                    self.player.camera_index = i+1
                    self.register_camera_flip()
                    self.set_message(f"Camera {i+1}", 1.0)
                    return

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse(*event.pos)
        elif event.type == pygame.KEYDOWN:
            # Doors
            if event.key == pygame.K_a:
                self.player.toggle_left()
                self.set_message("Left door toggled (A)", 1.5)
            elif event.key == pygame.K_d:
                self.player.toggle_right()
                self.set_message("Right door toggled (D)", 1.5)
            # Cameras toggle
            elif event.key == pygame.K_s:
                self.player.in_cameras = not self.player.in_cameras
                if self.player.in_cameras:
                    self.player.camera_index = 1
                    self.set_message("Entered cameras (S)", 1.0)
                else:
                    self.player.camera_index = 7
                    self.set_message("Returned to office", 1.0)
            # Numpad cameras
            elif event.key in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
                               pygame.K_KP4, pygame.K_KP5, pygame.K_KP6,
                               pygame.K_KP7]:
                if self.player.in_cameras:
                    self.player.camera_index = event.key - pygame.K_KP1 + 1
                    self.register_camera_flip()
                    self.set_message(f"Camera {self.player.camera_index}", 1.0)

    def set_message(self, msg, time_s=2.0):
        self.message = msg
        self.message_timer = time_s

    def register_camera_flip(self):
        now = time.time()
        if now - self.last_flip_time > 4.0:
            self.flip_count = 0
        self.flip_count += 1
        self.last_flip_time = now
        if getattr(self.golden, "visible", False) and self.flip_count >= 3:
            self.golden.visible = False
            self.flip_count = 0
            self.set_message("Golden Freddy vanished!", 1.5)

    # -----------------------
    # ATTACKS
    # -----------------------
    def resolve_attack(self, anim):
        if anim.name == "Bonnie":
            if self.player.left_door_closed:
                self.set_message("Bonnie blocked!", 1.5)
                anim.attacking = False
                anim.in_warning = False
            else:
                self.game_over("Bonnie")
        elif anim.name == "Chica":
            if self.player.right_door_closed:
                self.set_message("Chica blocked!", 1.5)
                anim.attacking = False
                anim.in_warning = False
            else:
                self.game_over("Chica")
        elif anim.name == "Freddy":
            if self.player.in_cameras and self.player.camera_index == anim.path[-1]:
                anim.attacking = False
                anim.in_warning = False
            else:
                self.game_over("Freddy")

    def resolve_foxy_attack(self):
        if self.foxy.attacking:
            if self.player.left_door_closed:
                self.set_message("Foxy dashed but blocked!", 1.5)
            else:
                self.player.hp -= 2
                self.set_message("Foxy got in!", 2.0)
            self.foxy.reset_charge()
            self.foxy.attacking = False
            self.foxy.running = False
            self.foxy.timer = 0

    # -----------------------
    # UPDATE
    # -----------------------
    def update_animatics(self, dt):
        dt_scaled = dt * self.night_speed_factor
        self.player.in_cameras = self.player.camera_index != 7

        for anim in self.animatronics:
            if anim.name == "Freddy":
                if not (self.player.in_cameras and self.player.camera_index == anim.path[-1]):
                    anim.timer += dt_scaled
            else:
                anim.update(dt_scaled, self.player)

            if anim.in_warning:
                anim.warning_time -= dt_scaled
                if anim.warning_time <= 0:
                    anim.in_warning = False
                    anim.path_idx += 1
                    anim.timer = 0
                    if anim.path_idx >= len(anim.path) - 1:
                        anim.attacking = True

            if anim.attacking:
                self.resolve_attack(anim)

        self.foxy.update(dt_scaled, self.player)
        self.resolve_foxy_attack()
        self.golden.update(dt_scaled, self.player)
        if getattr(self.golden,"visible",False) and self.player.camera_index == 7:
            if time.time() - self.last_flip_time > 3.5 / self.night_speed_factor:
                self.player.hp -= 1
                self.golden.visible = False
                self.set_message("Golden Freddy attacked!", 1.8)

    # -----------------------
    # DRAWING
    # -----------------------
    def draw_camera_view(self):
        cam = self.player.camera_index
        rect = CAM_RECTS[cam]
        pygame.draw.rect(self.screen, (12,12,12), rect)
        pygame.draw.rect(self.screen, (60,60,60), rect, 3)

        for anim in self.animatronics:
            if anim.path[anim.path_idx] == cam:
                w,h=90,180
                x=rect.x+(rect.width-w)//2
                y=rect.y+(rect.height-h)//2
                pygame.draw.rect(self.screen, anim.color, (x,y,w,h))
                if anim.in_warning:
                    lbl=FONT.render(f"{anim.name} WARNING!", True, anim.color)
                    self.screen.blit(lbl,(rect.x+20, rect.y+20))

        if cam==2:
            fx=pygame.Rect(rect.x+200,rect.y+60,120,220)
            pygame.draw.rect(self.screen,self.foxy.color,fx)
            lbl=FONT.render(f"Foxy stage {self.foxy.stage}/3",True,WHITE)
            self.screen.blit(lbl,(rect.x+16, rect.y+8))

    def draw_office_view(self):
        rect=CAM_RECTS[7]
        pygame.draw.rect(self.screen,(8,8,12),rect)
        pygame.draw.rect(self.screen,(60,60,60),rect,3)
        if getattr(self.golden,"visible",False):
            gf_rect=pygame.Rect(rect.x+200,rect.y+40,160,260)
            pygame.draw.rect(self.screen,(255,215,0),gf_rect)
            lbl=FONT.render("!!",True,(0,0,0))
            self.screen.blit(lbl,(gf_rect.x+gf_rect.width//2-6, gf_rect.y+gf_rect.height//2-12))

    # -----------------------
    # GAME OVER
    # -----------------------
    def game_over(self, anim_name):
        print(f"{anim_name} got you! GAME OVER")
        self.set_message(f"{anim_name} got you! GAME OVER",5.0)
        self.player.hp=0

    # -----------------------
    # MAIN LOOP
    # -----------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)/1000.0
            for event in pygame.event.get():
                self.handle_event(event)

            self.update_animatics(dt)

            # update in-game clock
            self.time_accumulator += dt * self.night_speed_factor
            while self.time_accumulator >= self.seconds_per_minute:
                self.time_accumulator -= self.seconds_per_minute
                self.minute += 1
                if self.minute >= 60:
                    self.minute = 0
                    self.hour += 1
                if self.hour > 6:
                    self.set_message("Congratulations! You survived the night!", 5.0)
                    self.running = False

            self.screen.fill((0,0,0))
            if self.player.in_cameras:
                self.draw_camera_view()
            else:
                self.draw_office_view()

            self.ui.draw(self.screen, self.player, self.message)

            # draw clock
            time_label = FONT.render(f"{self.hour:02d}:{int(self.minute):02d} AM", True, (255,255,255))
            self.screen.blit(time_label, (WIDTH-150, 20))

            if self.message_timer > 0:
                self.message_timer -= dt
                if self.message_timer <= 0:
                    self.message = ""

            pygame.display.flip()

            if self.player.hp <= 0:
                pygame.time.wait(2500)
                self.running = False

        pygame.quit()


if __name__=="__main__":
    Game().run()
