
import random
from config import *
from lane import GrassLane, RoadLane, RiverLane, RailLane

class WorldGenerator:
    def __init__(self):
        self.lanes = []
        self.next_y = 0 # Starting Y
        self.lane_index = 0
        
        # Initial safe zone
        for i in range(5):
            self.add_lane('grass_safe')
            
    def update(self, camera_y, dt):
        # Cull old lanes
        # If lane is far below camera
        # Camera is following negative Y. Screen height is H.
        # Bottom of screen is camera.scroll_y + SCREEN_HEIGHT
        # We cull if lane.y > camera.scroll_y + SCREEN_HEIGHT + Buffer
        
        cull_threshold = camera_y + SCREEN_HEIGHT + 200
        self.lanes = [l for l in self.lanes if l.y < cull_threshold]
        
        # Generate new lanes
        # Top of screen is camera.scroll_y
        # We want to generate up to camera.scroll_y - Buffer
        gen_threshold = camera_y - 100
        
        while self.next_y > gen_threshold:
            self.generate_next_batch()
            
        # Update lanes
        for lane in self.lanes:
            lane.update(dt)

    def add_lane(self, lane_type, difficulty_multiplier=1.0):
        if lane_type == 'grass_safe':
            l = GrassLane(self.next_y, self.lane_index)
            l.entities = [] # Clear obstacles
        elif lane_type == 'grass':
            l = GrassLane(self.next_y, self.lane_index)
        elif lane_type == 'road':
            speed = 100 + (self.lane_index * 0.5) # Scale speed
            l = RoadLane(self.next_y, self.lane_index, speed=speed, direction=random.choice([-1, 1]))
        elif lane_type == 'river':
            speed = 80 + (self.lane_index * 0.4)
            l = RiverLane(self.next_y, self.lane_index, speed=speed, direction=random.choice([-1, 1]))
        elif lane_type == 'rail':
             l = RailLane(self.next_y, self.lane_index)
             
        self.lanes.append(l)
        self.next_y -= TILE_SIZE
        self.lane_index += 1

    def generate_next_batch(self):
        # Weighted random choice for "Biome"
        # Biomes: Field (Grass), Highway (Roads), Water (Rivers), Track (Rails)
        
        choice = random.random()
        difficulty = 1.0 + (abs(self.next_y) / 5000.0) # Scale with distance
        
        if choice < 0.4: # 40% Grass
            count = random.randint(1, 4)
            for _ in range(count): self.add_lane('grass')
        elif choice < 0.7: # 30% Road
            count = random.randint(1, 5)
            for _ in range(count): self.add_lane('road')
        elif choice < 0.9: # 20% Water
            count = random.randint(1, 4)
            for _ in range(count): self.add_lane('river')
        else: # 10% Rail
            self.add_lane('rail')
            
    def get_lanes(self):
        return self.lanes
