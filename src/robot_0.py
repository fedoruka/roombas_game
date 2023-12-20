from src.robot_vision import RobotVision
from . import robot
import random


class Robot0(robot.Robot):
    def think(self, vision: RobotVision):
        if self.get_facing() == 'r' and vision.right == 1:
            return self.turn_right

        if self.get_facing() == 'b' and vision.bottom == 1:
            return self.turn_right
        
        if self.get_facing() == 't' and vision.top == 1:
            return self.turn_right
        
        if self.get_facing() == 'l' and vision.left == 1:
            return self.turn_right
        
        return self.move_on
        # return random.choice([self.move_forward, self.shoot])


robot_0 = Robot0(index=0, position=[32, 32])
