import pygame
import sys
from utils import load_data
from pages import pages
from actions import action
from actions import components
from sounds import sound
from player import player

"""
####################################################################
##                          _ooOoo_                               ##
##                         o8888888o                              ##
##                         88" . "88                              ##
##                         (| ^_^ |)                              ##
##                         O\  =  #O                              ##
##                      ____#`---'\____                           ##
##                    .'  \\|     |##  `.                         ##
##                   #  \\|||  :  |||##  \                        ##
##                  #  _||||| -:- |||||-  \                       ##
##                  |   | \\\  -  ### |   |                       ##
##                  | \_|  ''\---#''  |   |                       ##
##                  \  .-\__  `-`  ___#-. #                       ##
##                ___`. .'  #--.--\  `. . ___                     ##
##              ."" '<  `.___\_<|>_#___.'  >'"".                  ##
##            | | :  `- \`.;`\ _ #`;.`# - ` : | |                 ##
##            \  \ `-.   \_ __\ #__ _#   .-` #  #                 ##
##      ========`-.____`-.___\_____#___.-`____.-'========         ##
##                           `=---='                              ##
##      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        ##
##              佛祖保佑       永无BUG     永不修改               ##
####################################################################
"""
class Main:
    def __init__(self):
        # 分辨率
        self.resolution = self.resolution_width, self.resolution_height = (1280, 720)
        # 屏幕对象
        self.screen = pygame.display.set_mode(self.resolution)
        
        pygame.init()
        # 窗口标题
        pygame.display.set_caption("Nautical")
        # Logo
        pygame.display.set_icon(pygame.image.load(
            '_assets/logo.png').convert_alpha())
        #帧率
        self.clock = pygame.time.Clock()
        self.fps = 120
        # debug mode
        self.debug = False
        self.running = True
        
        self.router = "startmenu"
        self.showdialog = ""
        self.map = 0
        
        self.gameover_reason = ""
        
        self.data = load_data.Data()
        
        # 连接 Class
        self.BackgroundMusic = sound.BackgroundMusic(self)
        self.player = player.Player(self)
        self.Components = components.Comp(self)
        self.pages = pages.Pages(self)
        self.MainActions = action.MainActions(self)
        self.DrawActions = action.DrawActions(self)


    def run_loop(self):
        while self.running:
            self.MainActions.action()
            self.DrawActions.action()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.Components.onClick(event.pos)
                    if self.router == "nautical":
                        self.pages.nautical.click_action(event.pos)
                    
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main = Main()
    main.run_loop()
    pygame.quit()
    sys.exit()