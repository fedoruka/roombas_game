from . import robot


class Robot1(robot.Robot):
    def think(self, vision):
        if vision.bottom == 1 and vision.right == 1 and self.get_facing() != 't':
            return self.turn_left

        return self.move_forward


robot_1 = Robot1(index=1, position=[32 * 23, 32 * 16])
