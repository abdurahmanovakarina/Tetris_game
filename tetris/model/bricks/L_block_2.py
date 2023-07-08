from .L_block import LBlock


class LBlock2(LBlock):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_name(self):
        return "LBlock2"

    def get_arm_direction(self):
        return -1
