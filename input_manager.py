
import pygame

class InputManager:
    def __init__(self):
        self.actions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'quit': False,
            'confirm': False
        }
        self.previous_key_state = {}

    def update(self):
        # Reset one-shot actions
        for key in self.actions:
            self.actions[key] = False

        # Event Loop Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.actions['quit'] = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.actions['up'] = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.actions['down'] = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.actions['left'] = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.actions['right'] = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.actions['confirm'] = True
                elif event.key == pygame.K_ESCAPE:
                    self.actions['quit'] = True

    def get_action(self, action_name):
        return self.actions.get(action_name, False)
