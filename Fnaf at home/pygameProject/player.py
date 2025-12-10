# player.py
class Player:
    def __init__(self):
        self.camera_index = 7  # start in office
        self.in_cameras = False
        self.left_door_closed = False
        self.right_door_closed = False
        self.hp = 2
        self.power = 100

    def toggle_left(self):
        self.left_door_closed = not self.left_door_closed

    def toggle_right(self):
        self.right_door_closed = not self.right_door_closed

    def drain(self):
        drain_amount = 0
        if self.left_door_closed:
            drain_amount += 0.1
        if self.right_door_closed:
            drain_amount += 0.1
        self.power = max(0, self.power - drain_amount)
