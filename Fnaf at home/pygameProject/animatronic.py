class BaseAnimatronic:
    def __init__(self, name, color, path, move_time=10):
        self.name = name
        self.color = color
        self.path = path

        self.move_time = move_time
        self.timer = 0
        self.in_warning = False

        self.warning_time = 0
        self.path_idx = 0
        self.attacking = False

    def update(self, dt, player):
        if self.attacking:
            return

        self.timer += dt

        if self.timer >= self.move_time:
            self.timer = 0
            self.in_warning = True
            self.warning_time = 2.5  # reaction window


    def advance(self):
        self.in_warning = False
        self.path_idx += 1
        if self.path_idx >= len(self.path) - 1:
            self.attacking = True


class Foxy:
    def __init__(self):
        self.name = "Foxy"
        self.color = (255, 60, 60)

        self.stage = 1
        self.timer = 0
        self.stage_time = 18

        self.running = False
        self.attacking = False
        self.warning_time = 0

    def update(self, dt, player):
        if player.in_cameras and player.camera_index == 2:
            self.timer = 0
            return

        if not self.running and not self.attacking:
            self.timer += dt
            if self.timer >= self.stage_time:
                self.timer = 0
                self.stage += 1

                if self.stage >= 4:
                    self.running = True
                    self.warning_time = 2.5

        if self.running:
            self.warning_time -= dt
            if self.warning_time <= 0:
                self.running = False
                self.attacking = True

    def reset(self):
        self.stage = 1
        self.timer = 0
        self.running = False
        self.attacking = False