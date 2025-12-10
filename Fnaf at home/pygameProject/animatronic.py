import pygame
import random

class BaseAnimatronic:
    def __init__(self, name, color, path, move_time=5):
        self.name = name
        self.color = color
        self.path = path  # list of camera indices
        self.path_idx = 0
        self.move_time = move_time  # seconds to move to next cam
        self.timer = 0
        self.attacking = False
        self.in_warning = False
        self.warning_time = 2.0  # seconds of warning

    def update(self, dt, player):
        if self.attacking:
            return

        self.timer += dt
        if self.timer >= self.move_time:
            self.in_warning = True
            self.warning_time = 3.0 + random.uniform(0, 1.0)  # 3–4 seconds
            self.timer = 0

class Foxy(BaseAnimatronic):
    def __init__(self):
        super().__init__("Foxy", (255,0,0), [2], move_time=0)
        self.stage = 0
        self.running = False
        self.attacking = False
        self.timer = 0

    def update(self, dt, player):
        if self.stage < 3:
            # Foxy charges slowly while player not watching camera 2
            if not (player.in_cameras and player.camera_index==2):
                self.timer += dt
                if self.timer > 4.0:
                    self.stage += 1
                    self.timer = 0
        else:
            self.attacking = True

    def reset_charge(self):
        self.stage = 0
        self.timer = 0

class GoldenFreddy(BaseAnimatronic):
    def __init__(self):
        super().__init__("Golden Freddy", (255,215,0), [7], move_time=0)
        self.visible = False
        self.spawn_timer = 15  # seconds until first possible spawn

    def update(self, dt, player):
        if not self.visible:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.visible = True
                # randomize next appearance
                self.spawn_timer = random.randint(45, 60)
