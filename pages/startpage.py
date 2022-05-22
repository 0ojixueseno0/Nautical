import pygame
import sys
from pages.components import Notify

class StartPage:
    def __init__(self, this):
        self.this = this
        self.init()
        
    def init(self):
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
            .convert_alpha(), (360, 181)
        )
        self.startbtn = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/startbtn.png")
            .convert_alpha(), (96, 42)
        )
        self.continuebtn = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/continuebtn.png")
            .convert_alpha(), (96, 42)
        )
        self.continuebtn_disable = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/continuebtn_disable.png")
            .convert_alpha(), (96, 42)
        )
        # self.helpbtn = pygame.transform.scale(
        #     pygame.image.load("./_assets/startmenu/helpbtn.png")
        #     .convert_alpha(), (96, 42)
        # )
        self.exitbtn = pygame.transform.scale(
            pygame.image.load("./_assets/startmenu/exitbtn.png")
            .convert_alpha(), (96, 42)
        )
        
        self.cloudbg_rect = self.cloudbg.get_rect()
        self.cloudbg_copied_rect = self.cloudbg_copied.get_rect()
        self.seabg_rect = self.seabg.get_rect()
        self.seabg_copied_rect = self.seabg_copied.get_rect()
        
        self.buildComponent()
        
        self.x1 = 0
        self.x2 = self.x1 + self.cloudbg_copied_rect.width
        self.z1 = 0
        self.z2 = self.z1 + self.seabg_copied_rect.width
        self.rollspeed = 0.2
        self.this.BackgroundMusic.startmenu_play()
        self.shownotify = False
        self.notify = None
        pass
    
    def buildComponent(self):
        startbtn_rect = self.startbtn.get_rect()
        startbtn_rect.x, startbtn_rect.y = 592, 375
        self.this.Components.addComponent(
            startbtn_rect, 
            self.onstart,
            router="startmenu"
            )
        
        continuebtn_rect = self.continuebtn.get_rect()
        continuebtn_rect.x, continuebtn_rect.y = 592, 438
        self.this.Components.addComponent(
            continuebtn_rect, 
            self.oncontinue,
            router="startmenu"
            )
        
        # helpbtn_rect = self.helpbtn.get_rect()
        # helpbtn_rect.x, helpbtn_rect.y = 592, 454
        # self.this.Components.addComponent(
        #     helpbtn_rect, 
        #     self.help,
        #     router="startmenu"
        #     )
        
        exitbtn_rect = self.exitbtn.get_rect()
        exitbtn_rect.x, exitbtn_rect.y = 592, 501
        self.this.Components.addComponent(
            exitbtn_rect, 
            self.onexit,
            router="startmenu"
            )
    
    # def help(self):
    #     if self.shownotify == False:
    #         self.this.pages.help.init()
    #         self.this.router = "help"
    #         pass
    
    def notiNotify(self):
        self.notify = Notify(self.this,
                             title="提示",
                             content="你有已保存的游戏进度，点击继续将覆盖已有游戏进度",
                             btn_no_func=self.notify_no,
                             btn_yes_func=self.notify_yes,
                             yes_label="继续",
                             no_label="返回",
                             router="startmenu")
        self.shownotify = True
    
    def gowharf(self):
        self.this.player.reset_player()
        self.this.Components.clear()
        self.this.pages.darken_screen()
        self.this.pages.wharf.init()
        self.this.router = "wharf"
        
    
    def notify_yes(self):
        self.this.player.reset_player()
        self.notify_no()
        self.gowharf()
    
    def notify_no(self):
        self.notify.delete()
        self.notify = None
        self.shownotify = False
    
    def oncontinue(self):
        if self.this.player.inMap and self.shownotify == False and len(self.this.player.map) > 1:
            self.this.map = self.this.player.map["mapid"]
            self.this.pages.darken_screen()
            self.this.router = "nautical"
            self.this.BackgroundMusic.startmenu_stop()
            self.this.pages.nautical.continue_game = True
            self.this.pages.nautical.init(self.this)
            self.this.BackgroundMusic.game_music_play()
    
    def onstart(self):
        if self.shownotify == False:
            if self.this.player.inMap:
                self.notiNotify()
            else:
                self.gowharf()
            # self.this.BackgroundMusic.startmenu_stop()
    
    def onexit(self):
        if self.shownotify == False:
            pygame.quit()
            sys.exit()
    
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
        self.this.screen.blit(self.logo, (460, 158))
        self.this.screen.blit(self.startbtn, (592, 375))
        self.this.screen.blit(self.continuebtn_disable, (592, 438))
        if self.this.player.inMap and len(self.this.player.map)>1:
            self.this.screen.blit(self.continuebtn, (592, 438))
        # self.this.screen.blit(self.helpbtn, (592, 454))
        self.this.screen.blit(self.exitbtn, (592, 501))
        if self.shownotify:
            self.notify.draw_action()

