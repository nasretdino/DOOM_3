import math

RES = WIDTH, HEIGHT = 1600, 900
FPS = 120

CELL_PIXELS = 100


PLAYER_POS = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_SIZE_SCALE = 60


FOV = 60  # должно быть четным
HALF_FOV = FOV / 2
NUM_RAYS_FOV = WIDTH
DELTA_ANGLE = FOV / NUM_RAYS_FOV
MAX_DEPTH = 20 # зависит от ширины экрана и размера клетки

PLAYER_ROT_SPEED = DELTA_ANGLE * 2 # может быть только больше или равен DELTA_ANGLE
SCALE = NUM_RAYS_FOV // WIDTH


SCREEN_DIST = (WIDTH / 2) / math.tan(math.radians(HALF_FOV))


