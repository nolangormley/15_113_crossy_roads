
import pygame
import random
from config import *
from vehicles import Vehicle, Train
from environment import Obstacle, Log

class Lane:
    def __init__(self, y_pos, index):
        self.y = y_pos
        self.index = index
        self.entities = []
        self.type = "grass"
        
    def update(self, dt):
        # Update all entities
        for e in self.entities:
            e.update(dt)
            
        # Remove off-screen entities
        # Assuming world width is somewhat finite or we cull far off entities
        # But we need infinite horizontal for scrolling? 
        # Actually Crossy Road is bounded horizontally usually ~15-20 tiles wide
        # Entities spawn from one side and exit the other.
        self.entities = [e for e in self.entities if -200 < e.x < SCREEN_WIDTH + 200]
        
    def render_background(self, surface, camera):
        screen_y = camera.apply(self.y)
        if -TILE_SIZE < screen_y < SCREEN_HEIGHT:
            color = COLOR_GRASS
            if self.type == 'road': color = COLOR_ROAD
            elif self.type == 'river': color = COLOR_RIVER
            elif self.type == 'rail': color = COLOR_RAIL
            
            # Alternating grass color for style
            if self.type == 'grass' and self.index % 2 == 0:
                color = COLOR_GRASS_LIGHT
                
            rect = pygame.Rect(0, screen_y, SCREEN_WIDTH, TILE_SIZE)
            pygame.draw.rect(surface, color, rect)
            
            # Extra details
            if self.type == 'road':
                # Dash lines
                pygame.draw.line(surface, COLOR_ROAD_MARKING, (0, screen_y + TILE_SIZE - 2), (SCREEN_WIDTH, screen_y + TILE_SIZE - 2), 2)
            elif self.type == 'rail':
                # Ties
                for i in range(0, SCREEN_WIDTH, 20):
                    pygame.draw.rect(surface, COLOR_RAIL_METAL, (i, screen_y + 2, 4, TILE_SIZE - 4))
                pygame.draw.line(surface, COLOR_RAIL_METAL, (0, screen_y + 10), (SCREEN_WIDTH, screen_y + 10), 4)
                pygame.draw.line(surface, COLOR_RAIL_METAL, (0, screen_y + TILE_SIZE - 10), (SCREEN_WIDTH, screen_y + TILE_SIZE - 10), 4)


class GrassLane(Lane):
    def __init__(self, y_pos, index):
        super().__init__(y_pos, index)
        self.type = 'grass'
        self.obstacle_chance = 0.2
        self.setup_obstacles()
        
    def setup_obstacles(self):
        # Spawn random trees, leaving at least one path open
        # We need a guaranteed path? Not necessarily per lane, but overall connectivity.
        # But for simple reliable generation, just random holes.
        for i in range(COLUMNS):
            if random.random() < self.obstacle_chance:
                # Calculate X based on column index
                x = i * (SCREEN_WIDTH / COLUMNS) # Align to grid
                self.entities.append(Obstacle(x, self.y))

class RoadLane(Lane):
    def __init__(self, y_pos, index, speed=100, direction=1):
        super().__init__(y_pos, index)
        self.type = 'road'
        self.direction = direction # 1 or -1
        self.speed = speed * direction
        self.spawn_timer = 0
        self.spawn_interval = 2.0 # Variable
        self.min_interval = 1.5
        
        # Difficulty scaling could happen here
        
    def update(self, dt):
        super().update(dt)
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_vehicle()
            self.spawn_timer = random.uniform(self.min_interval, self.min_interval * 2)
            
    def spawn_vehicle(self):
        width = TILE_SIZE * 1.5
        start_x = -width if self.direction == 1 else SCREEN_WIDTH
        v = Vehicle(start_x, self.y, width, self.speed)
        self.entities.append(v)

class RiverLane(Lane):
    def __init__(self, y_pos, index, speed=80, direction=-1):
        super().__init__(y_pos, index)
        self.type = 'river'
        self.direction = direction
        self.speed = speed * direction
        self.spawn_timer = 0
        self.spawn_interval = 2.0
        
    def update(self, dt):
        super().update(dt)
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_log()
            self.spawn_timer = random.uniform(1.5, 3.0)
            
    def spawn_log(self):
        size_mult = random.choice([2, 3, 4])
        width = TILE_SIZE * size_mult
        start_x = -width if self.direction == 1 else SCREEN_WIDTH
        l = Log(start_x, self.y, width, self.speed)
        self.entities.append(l)

class RailLane(Lane):
    def __init__(self, y_pos, index):
        super().__init__(y_pos, index)
        self.type = 'rail'
        self.train_timer = random.uniform(5, 10)
        self.train_active = False # Warning state
        self.train_passing = False
        self.warning_duration = 2.0
        self.warning_timer = 0
        
    def update(self, dt):
        super().update(dt)
        
        if not self.train_active and not self.train_passing:
            self.train_timer -= dt
            if self.train_timer <= 0:
                self.train_active = True
                self.warning_timer = self.warning_duration
                # Play warning sound
        
        elif self.train_active:
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                self.train_active = False
                self.spawn_train()

    def spawn_train(self):
        self.train_passing = True
        direction = random.choice([-1, 1])
        speed = 800 * direction
        width = TILE_SIZE * 15
        start_x = -width if direction == 1 else SCREEN_WIDTH
        t = Train(start_x, self.y, speed)
        self.entities.append(t)
        
    def render_background(self, surface, camera):
        super().render_background(surface, camera)
        screen_y = camera.apply(self.y)
        if self.train_active:
            # Draw warning lights
            color = (255, 0, 0)
            if int(pygame.time.get_ticks() / 200) % 2 == 0:
                color = (100, 0, 0)
            pygame.draw.circle(surface, color, (50, screen_y + 5), 5)
            pygame.draw.circle(surface, color, (SCREEN_WIDTH - 50, screen_y + 5), 5)

