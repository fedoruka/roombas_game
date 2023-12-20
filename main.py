import pygame

from src.robot_0 import robot_0
from src.robot_1 import robot_1
from src.robot_2 import robot_2
from src.robot_3 import robot_3
from src.tiles import BLOCKING_TILES


robots = [
    robot_0, 
    robot_1, 
    robot_2, 
    robot_3, 
]
bullets = []


pygame.init()

# Set the dimensions of each tile
TILE_SIZE = 32

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Calculate the number of tiles in each dimension
TILES_X = WINDOW_WIDTH // TILE_SIZE
TILES_Y = WINDOW_HEIGHT // TILE_SIZE

# Load the images
images = {
    0: pygame.image.load('images/land.png'),
    1: pygame.image.load('images/wall.png'),
    2: pygame.image.load('images/water.png'),
    3: pygame.image.load('images/bomb.png'),
    4: pygame.image.load('images/medikit.png'),
}

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Generate a randomized tilemap
tilemap = []


with open('map.txt', 'r') as f:
    tilemap = [[int(num) for num in line.split()] for line in f]


clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the tilemap
    for y in range(TILES_Y):
        for x in range(TILES_X):
            window.blit(images[tilemap[y][x]], (x * TILE_SIZE, y * TILE_SIZE))

    for bullet in bullets:
        bullet.move()
        bullet.draw(window)
        for robot in robots:
            if bullet.active is True and pygame.Rect(robot.position, (TILE_SIZE, TILE_SIZE)).collidepoint(bullet.position):
                bullet.active = False
                robot.health -= 100
    
    bullets = [obj for obj in bullets if obj.active]

    for robot in robots:
        window.blit(robot.get_tile(), (robot.position[0] , robot.position[1]))

        health_text = pygame.font.Font(None, 25).render(str(f"{robot.health} {robot.position[0]}:{robot.position[1]}"), True, (0, 255, 0))
        window.blit(health_text, (robot.position[0], robot.position[1] - 25))

        vision = robot.get_surrounding_tiles(TILES_X * 32, TILES_Y * 32, tilemap)

        action = robot.think(vision)
        result = action()

        if result is not None:
            bullets.append(result)

        if robot.position[1] % 32 == 0 and robot.position[0] % 32 == 0:
            if robot.facing == 'b' and vision.bottom in BLOCKING_TILES: 
                robot.can_move_forward = False
            elif robot.facing == 't' and vision.top in BLOCKING_TILES: 
                robot.can_move_forward = False
            elif robot.facing == 'l' and vision.left in BLOCKING_TILES: 
                robot.can_move_forward = False
            elif robot.facing == 'r' and vision.right in BLOCKING_TILES: 
                robot.can_move_forward = False
            else: 
                robot.can_move_forward = True
                
            if vision.current_tile == 2:  # water
                robot.health -= 100

            if vision.current_tile == 3:  # bomb
                tilemap[vision.current_tiles_x_y[1]][vision.current_tiles_x_y[0]] = 0
                robot.health -= 250

            if vision.current_tile == 4:  # medikit
                tilemap[vision.current_tiles_x_y[1]][vision.current_tiles_x_y[0]] = 0
                robot.health = min(robot.health + 100, 1000)

        robot.move_forward()

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
