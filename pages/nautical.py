import pygame

class Nautical:
    def __init__(self, this):
        self.this = this
        
        self.background = pygame.transform.scale(
            pygame.image.load(f"_assets/maps/{this.map}.png"),
            this.resolution
        )
        