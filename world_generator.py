
import random
from config import *
from lane import GrassLane, RoadLane, RiverLane, RailLane

class WorldGenerator:
    def __init__(self):
        self.lanes = []
        self.next_y = 0 # Starting Y
        self.lane_index = 0
        
        self.last_biome = None

        # Initial safe zone
        for i in range(5):
            self.add_lane('grass_safe')
            self.last_biome = 'grass'
            
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

    def add_lane(self, lane_type, difficulty_multiplier=1.0, direction_override=None):
        if lane_type == 'grass_safe':
            l = GrassLane(self.next_y, self.lane_index)
            l.entities = [] # Clear obstacles
        elif lane_type == 'grass':
            l = GrassLane(self.next_y, self.lane_index)
        elif lane_type == 'road':
            speed = 100 + (self.lane_index * 0.5) # Scale speed
            direction = direction_override if direction_override is not None else random.choice([-1, 1])
            l = RoadLane(self.next_y, self.lane_index, speed=speed, direction=direction)
        elif lane_type == 'river':
            speed = 80 + (self.lane_index * 0.4)
            direction = direction_override if direction_override is not None else random.choice([-1, 1])
            l = RiverLane(self.next_y, self.lane_index, speed=speed, direction=direction)
        elif lane_type == 'rail':
             l = RailLane(self.next_y, self.lane_index)
             
        self.lanes.append(l)
        self.next_y -= TILE_SIZE
        self.lane_index += 1

    def generate_next_batch(self):
        # Biomes: Field (Grass), Highway (Roads), Water (Rivers), Track (Rails)
        # Ensure we don't repeat the same biome to keep sizes restrained
        
        available_biomes = ['grass', 'road', 'river', 'rail']
        
        # Simple weighted selection logic that respects "don't repeat"
        if self.last_biome in available_biomes:
            available_biomes.remove(self.last_biome)
            
        choice = random.choice(available_biomes)
        
        # Difficulty scaling could adjust specific params, but type selection is now uniform among remaining
        
        if choice == 'grass':
            count = random.randint(3, 5)
            for _ in range(count): self.add_lane('grass')
            self.last_biome = 'grass'
            
        elif choice == 'road':
            count = random.randint(3, 5)
            for _ in range(count): self.add_lane('road')
            self.last_biome = 'road'
            
        elif choice == 'river':
            count = random.randint(3, 5)
            # Alternate flow direction for adjacent rivers
            start_dir = random.choice([-1, 1])
            for i in range(count): 
                # i=0 -> start_dir, i=1 -> -start_dir, etc.
                direction = start_dir * (1 if i % 2 == 0 else -1)
                
                # We need to modify add_lane to accept explicit direction for river
                # Currently add_lane randomizes it internally for river/road if not exposed.
                # Let's override it by modifying add_lane signature or just hacking it here.
                # Actually `add_lane` generates the lane object.
                # Let's extract the creation logic or pass kwargs.
                self.add_lane('river', direction_override=direction)
                
            self.last_biome = 'river'
            
        elif choice == 'rail':
            # Rails are usually single or distinct.
            self.add_lane('rail')
            self.last_biome = 'rail'
            
    def get_lanes(self):
        return self.lanes
