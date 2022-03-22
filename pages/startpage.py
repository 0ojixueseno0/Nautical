import pygame

class StartPage:
    def __init__(self, this):
        self.this = this
        self.cloudbg = self.cloudbg_copied = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/cloudbg.png")
            .convert_alpha(), (1280, 720)
        )
        self.seabg = self.seabg_copied = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/seabg.png")
            .convert_alpha(), (1280, 240)
        )
        self.logo = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/logo.png")
            .convert_alpha(), (322, 161)
        )
        self.startbtn = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/startbtn.png")
            .convert_alpha(), (96, 42)
        )
        self.cloudbg_rect = self.cloudbg.get_rect()
        self.cloudbg_copied_rect = self.cloudbg_copied.get_rect()
        self.seabg_rect = self.seabg.get_rect()
        self.seabg_copied_rect = self.seabg_copied.get_rect()
        startbtn_rect = self.startbtn.get_rect()
        
        startbtn_rect.x, startbtn_rect.y = 592, 395
        self.this.Components.addComponent(startbtn_rect, self.onbtnclick)
        
        self.x1 = 0
        self.x2 = self.x1 + self.cloudbg_copied_rect.width
        self.z1 = 0
        self.z2 = self.z1 + self.seabg_copied_rect.width
        self.rollspeed = 0.2
        this.BackgroundMusic.startmenu_play()
        pass

    def onbtnclick(self):
        self.this.pages.darken_screen()
        # self.this.BackgroundMusic.startmenu_stop()
        self.this.router = "wharf"
        
    def rollbg_action(self):
        self.x1 -= self.rollspeed
        self.x2 -= self.rollspeed
        self.z1 -= self.rollspeed + 0.2
        self.z2 -= self.rollspeed + 0.2
        if self.x1 + 1280 <= 0:
            self.x1 = self.x2 + self.cloudbg_rect.width
        if self.x2 + 1280 <= 0:
            self.x2 = self.x1 + self.cloudbg_copied_rect.width
        if self.z1 + 1280 <= 0:
            self.z1 = self.z2 + self.seabg_rect.width
        if self.z2 + 1280 <= 0:
            self.z2 = self.z1 + self.seabg_copied_rect.width
        pass
    
    def draw_action(self):
        self.this.screen.blit(self.cloudbg, (self.x1, 0))
        self.this.screen.blit(self.cloudbg_copied, (self.x2, 0))
        self.this.screen.blit(self.seabg, (self.z1, 480))
        self.this.screen.blit(self.seabg_copied, (self.z2, 480))
        self.this.screen.blit(self.logo, (479, 199))
        self.this.screen.blit(self.startbtn, (592, 395))
        