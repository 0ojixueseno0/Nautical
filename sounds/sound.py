
import pygame


class BackgroundMusic:
    def __init__(self, this):
        self.this = this
        self.ocean_music = "./_assets/sounds/ocean.ogg"
        # self.flyinglow = "./_assets/sounds/deepsea.ogg"
        self.flyinglow = "./_assets/sounds/flyinglow.ogg"
        self.seagull = "./_assets/sounds/seagull.ogg" # 海鸥
        self.sea_effect = pygame.mixer.Sound("./_assets/sounds/seaeffect.ogg") # 海浪
        self.piracy = pygame.mixer.Sound("./_assets/sounds/piracy.ogg")
        self.volume = 0.5
        
        self.editor_music = "./_assets/sounds/editor.ogg"
    
    def play_piracy(self):
        pygame.mixer.init()
        self.sea_effect.play(loops=1)

        pass
    
    def game_music_play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.ocean_music)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
    
    def editor_play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.editor_music)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
    
    def startmenu_play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.flyinglow)
        pygame.mixer.music.set_volume(0.5)
        self.sea_effect.set_volume(0.5)
        self.sea_effect.play(-1)
        # pygame.mixer.music.load(self.sea_effect)
        pygame.mixer.music.play(-1)
    
    def startmenu_stop(self):
        for i in range(int(self.volume*10))[::-1]:
            pygame.mixer.music.set_volume(i/10)
            # self.sea_effect.set_volume(i/10)
            pygame.time.delay(100)
        pygame.mixer.music.stop()
        # self.sea_effect.stop()
        pygame.mixer.init()