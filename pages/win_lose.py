import pygame

from pages.components import Dialog


class win_lose:
    def __init__(self, this):
        self.this = this
    
    def init(self):
        self.this.player.clear()
        this = self.this
        self.cloudbg = self.cloudbg_copied = pygame.transform.scale(
            pygame.image.load("./_assets/wharf/cloudbg.png")
            .convert_alpha(), (1280, 720)
        )
        self.cloudbg_rect = self.cloudbg.get_rect()
        self.cloudbg_copied_rect = self.cloudbg_copied.get_rect()
        
        self.coastbg = pygame.transform.scale(
            pygame.image.load("./_assets/wharf/coastbg.png")
            .convert_alpha(), (1280, 605)
        )
        self.x1 = 0
        self.x2 = self.x1 + self.cloudbg_copied_rect.width
        self.rollspeed = 0.2
        
        self.dialog = Dialog(this, "游戏结束")
        
        font = pygame.font.Font("_assets/pixelfont.ttf", 30)
        self.reason = font.render(this.gameover_reason, True, (255, 255, 255))
        self.reason_rect = self.reason.get_rect()
        
        font = pygame.font.Font("_assets/pixelfont.ttf", 20)
        self.btn_label = [
            font.render("重新开始", True, (0, 0, 0)),
            font.render("退出游戏", True, (0, 0, 0))
        ]
        self.btn_bg = pygame.transform.scale(
            pygame.image.load("_assets/component/btn.png")
            .convert_alpha(), (124,72)
        )
        self.btn_bg_rect = self.btn_bg.get_rect()
        self.btn_bg_rect.x = 492
        self.btn_bg_rect.y = 470
        self.exit_btn_rect = self.btn_bg_rect.copy()
        self.exit_btn_rect.x = 665
        this.Components.addComponent(
            self.btn_bg_rect,
            self.restart,
            router="win_lose"
        )
        this.Components.addComponent(
            self.exit_btn_rect,
            self.exitgame,
            router="win_lose"
        )
    
          
    def exitgame(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def restart(self):
        self.this.pages.darken_screen()
        self.this.player.clear()
        self.this.player.init()
        self.this.router = "startmenu"
        self.this.Components.components = []
        self.this.pages.startpage.init()
        pass
        
    def rollbg_action(self):
        self.x1 -= self.rollspeed
        self.x2 -= self.rollspeed
        if self.x1 + 1280 <= 0:
            self.x1 = self.x2 + self.cloudbg_rect.width
        if self.x2 + 1280 <= 0:
            self.x2 = self.x1 + self.cloudbg_copied_rect.width
    
    def draw_action(self):
        self.this.screen.blit(self.cloudbg, (self.x1, 0))
        self.this.screen.blit(self.cloudbg_copied, (self.x2, 0))
        self.this.screen.blit(self.coastbg, (0, 82))
        
        self.dialog.draw_action((
            self.this.resolution_width / 2 - self.dialog.dialog_rect.width / 2,
            self.this.resolution_height / 2 - self.dialog.dialog_rect.height / 2
        ))
        
        self.this.screen.blit(self.reason, (
            self.this.resolution_width / 2 - self.reason_rect.width / 2,
            self.this.resolution_height / 2 - self.reason_rect.height / 2
        ))
        
        self.this.screen.blit(self.btn_bg, (self.btn_bg_rect.x, self.btn_bg_rect.y))
        self.this.screen.blit(self.btn_bg, (self.exit_btn_rect.x, self.exit_btn_rect.y))
        self.this.screen.blit(self.btn_label[0], (
            self.btn_bg_rect.x+22, self.btn_bg_rect.y+26
        ))
        self.this.screen.blit(self.btn_label[1], (
            self.exit_btn_rect.x+22, self.exit_btn_rect.y+26
        ))
        