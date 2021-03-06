import math

# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PHEIGHT = 5 * HEIGHT
FPS = 10
TILE = 100
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE = 1 * MINIMAP_SCALE
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MINIMAP_SCALE)

STAMINA_POS = (5, 20)
HP_POS = (5, 50)

PUSHKA_POS = (WIDTH - 550, HEIGHT - 300)
# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

DOUBLE_PI = 2 * math.pi
CENTER_RAY = NUM_RAYS // 2 - 1
# texture settings (1200 x 1200)
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# player settings
player_pos = (138, 138)
player_angle = 0
player_speed = 2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (138, 0, 0)
GREEN = (0, 80, 0)
VYRVI_GLAZ = (83, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (235, 235, 235)
