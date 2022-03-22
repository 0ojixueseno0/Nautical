import pygame
from pages.nautical import Nautical
from pages.startpage import StartPage
from pages.wharf import Wharf
from pages.trade import Trade

class Pages:
    def __init__(self, this):
        self.this = this
        self.startpage = StartPage(this)
        self.wharf = Wharf(this)
        self.trade = Trade(this)
        self.nautical = Nautical(this)
        pass
    
    # 转场效果
    def darken_screen(self):
        BLACK = (0,0,0)
        dark_img = self.this.screen.convert_alpha()
        #  透明度（opacity）等于零0为完全不透明，等于255时为完全透明
        for opacity in range(0,255,15):
            self.this.clock.tick(self.this.fps)
            #  fill方法的第一个color参数需传入元组
            #  元组的前三个整数控制RGB数值，最后一个为透明度
            dark_img.fill((*BLACK,opacity))
            self.this.screen.blit(dark_img,(0,0))
            pygame.display.update()
            #  控制转场效果的速度
            pygame.time.delay(25)