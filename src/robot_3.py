from src.robot_vision import RobotVision
from . import robot

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
        
        return self.move_forward


robot_3 = Robot0(index=3, position=[32, 32 * 16])
