
import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Crossy Road Python"

# Grid / World
TILE_SIZE = 40  # Base size of a grid cell
GRID_WIDTH = 13 # Number of tiles horizontally
# The camera will center the player. 
# Virtual width is larger than screen to allow some margin? 
# Actually Crossy Road is fixed width usually.
# Let's align tile size to screen. 800 / 40 = 20 tiles wide.
COLUMNS = 20

# Colors
COLOR_BG = (135, 206, 235)  # Sky blue-ish
COLOR_GRASS = (109, 212, 126)
COLOR_GRASS_LIGHT = (121, 221, 137)
COLOR_ROAD = (85, 85, 85)
COLOR_ROAD_MARKING = (255, 255, 255)
COLOR_RIVER = (66, 179, 244)
COLOR_RAIL = (139, 69, 19)
COLOR_RAIL_METAL = (192, 192, 192)

# Entities
PLAYER_SPEED = 0.15 # Seconds per hop
PLAYER_COLOR = (255, 255, 255) # Chicken white

# Mechanics
SCROLL_SPEED_INITIAL = 30 # Pixels per second camera creep (if applicable) or player driven
GAME_SPEED_INCREASE = 0.05 # Multiplier per score bracket

# Z-Layers
LAYER_GROUND = 0
LAYER_WATER_OBJECT = 1 # Logs
LAYER_PLAYER = 2
LAYER_VEHICLE = 3
LAYER_OBSTACLE = 3 # Trees same as vehicles usually
LAYER_AIR = 4 # Birds?
LAYER_UI = 10
