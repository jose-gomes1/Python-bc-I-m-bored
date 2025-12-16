class Player:
    def __init__(self):
        self.power = 100
        self.music_box = 100
        self.left_door_closed = False
        self.right_door_closed = False
        self.in_cameras = False
        self.camera_index = 7
        self.hp = 2

    def toggle_left(self):
        self.left_door_closed = not self.left_door_closed

    def toggle_right(self):
        self.right_door_closed = not self.right_door_closed

    def drain_power(self, dt):
        drain = 0
        if self.left_door_closed: drain += 0.05
        if self.right_door_closed: drain += 0.05
        self.power = max(0, self.power - drain*dt)  # scale per second