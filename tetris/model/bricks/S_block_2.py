from .S_block import SBlock


class SBlock2(SBlock):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_name(self):
        return "SBlock2"

    def get_arm_direction(self):
        return -1
