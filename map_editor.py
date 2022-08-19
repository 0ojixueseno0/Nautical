import shutil
import pygame
import os
import json
import sys
from actions import components
from sounds import sound


class MapGenerator:
    def __init__(self, this):
        self.this = this
        maps = list(os.walk("./_assets/maps"))[0][2]
        for c in maps:
            if not os.path.isfile(f"./_data/maps/{c[:-4]}.json"):
                shutil.copyfile("./_data/maps/example.json", f"./_data/maps/{c[:-4]}.json")
        with open(f"./_data/maps/{this.map}.json") as f:
            self.mapconf = json.load(f)
        self.prop = self.mapconf["map"]["prop"].split(":")
        
        self.map_bg = pygame.transform.scale(
            pygame.image.load(self.mapconf["background"]),
            self.this.resolution
        )
        
        if self.mapconf["map"]["data"] == []:
            data = []
            for y in range(int(self.prop[1])):
                line = []
                for x in range(int(self.prop[0])):
                    line.append("0")
                data.append(line)
            self.mapdata = data
            pass
        else:
            self.mapdata = self.mapconf["map"]["data"]
        # print(self.mapdata)
        self.select = None
        
        self.coordinate()
            
        self.hover_bg =  pygame.Surface(
            (self.coordinate_width,self.coordinate_height),
            pygame.SRCALPHA)
        self.sel_bg = pygame.Surface(
            (self.coordinate_width,self.coordinate_height),
            pygame.SRCALPHA)
        self.special_bg = pygame.Surface(
            (self.coordinate_width,self.coordinate_height),
            pygame.SRCALPHA)
        self.special_bg.fill((0,128,0,128))
        self.hover_bg.fill((0,0,128,128))
        self.sel_bg.fill((128,0,0,128))
        
        font = pygame.font.Font("./_assets/pixelfont.ttf", self.coordinate_width//2)
        self.showtype = [font.render(f"{i}", True, (255,255,255)) for i in range(6)]
        
    def savemap(self):
        self.mapconf["map"]["data"] = self.mapdata
        with open(f"./_data/maps/{self.this.map}.json", "w") as f:
            f.write(json.dumps(self.mapconf, indent=4, ensure_ascii=False))
    
    def coordinate(self):
        self.coordinate_width = self.this.resolution[0] // int(self.prop[0])
        self.coordinate_height = self.this.resolution[1] // int(self.prop[1])
        pass
    
    def convert_pos(self, rawpos):
        x = rawpos[0] // self.coordinate_width
        y = rawpos[1] // self.coordinate_height
        return [x,y]
    
    def parse_pos(self, pos):
        x = pos[0] * self.coordinate_width
        y = pos[1] * self.coordinate_height
        return [x,y]
    
    def select_action(self, rawpos):
        pos = self.convert_pos(rawpos)
        self.select = None if pos == self.select else pos
        
    def confirm_action(self, type):
        if self.select is not None:
            self.mapdata[self.select[1]][self.select[0]] = type
    def setspawn(self):
        if self.select is not None:
            self.mapconf["spawn"]["x"] = self.select[0]
            self.mapconf["spawn"]["y"] = self.select[1]
            self.select = None
            #WIP: 出生点背景
        
    def draw_action(self):
        self.this.screen.blit(self.map_bg, (0, 0))
        for iy, y in enumerate(self.mapdata):
            for ix, x in enumerate(y):
                pygame.draw.rect(
                    self.this.screen, 
                    [0, 0, 0],
                    [
                        ix*self.coordinate_width,
                        iy*self.coordinate_height,
                        self.coordinate_width,
                        self.coordinate_height
                    ], 1)
                self.this.screen.blit(
                    self.showtype[int(x)],
                    ((ix+0.25)*self.coordinate_width,
                    (iy+0.25)*self.coordinate_height))
                if x != "0":
                    self.this.screen.blit(self.special_bg, (
                        ix*self.coordinate_width,
                        iy*self.coordinate_height,)
                    )
                
        
        self.this.screen.blit(self.hover_bg, self.parse_pos(self.convert_pos(self.this.pointer_pos)))
        if self.select is not None:
            self.this.screen.blit(self.sel_bg, self.parse_pos(self.select))
                                 
        pass

class actions:
    def __init__(self, this):
        self.this = this
        pass
    def draw_action(self):
        self.this.editor.draw_action()

class editor:
    def __init__(self, this):
        self.this = this
        font = pygame.font.Font("./_assets/pixelfont.ttf", 20)
        self.title = [
            font.render("Nautical 地图编辑器", True, (255,255,255)),
            font.render("点选方块后按下 数字键 进行标记", True, (255,255,255)),
            font.render("0: 默认状态, 背景区块", True, (255,255,255)),
            font.render("1: 路径", True, (255,255,255)),
            font.render("2: 岛屿区块A（判断点）", True, (255,255,255)),
            font.render("3: 岛屿区块B（判断点）", True, (255,255,255)),
            font.render("4: 岛屿区块C（判断点）", True, (255,255,255)),
            font.render("5: 设置出生点", True, (255,255,255)),
        ]
        self.intro_bg = pygame.Surface((330,170), pygame.SRCALPHA)
        self.intro_bg.fill((0,0,0,128))
        self.btn_save = font.render("保存修改", True, (255,255,255))
        self.btn_bg = pygame.Surface((90,30), pygame.SRCALPHA)
        self.btn_bg.fill((0,0,0,128))
        self.btn_bg_rect = self.btn_bg.get_rect()
        self.btn_bg_rect.x = 5
        self.btn_bg_rect.y = this.resolution_height-35
        this.components.addComponent(self.btn_bg_rect, self.save, router="editor")
        # windowSurface.blit(s, (0,0))
    def save(self):
        self.this.generator.savemap()

    def draw_action(self):
        self.this.screen.blit(self.intro_bg, (0,0))
        for i, t in enumerate(self.title):
            self.this.screen.blit(t, (5, i*20+5))
        self.this.screen.blit(self.btn_bg, (5, self.this.resolution_height-35))
        self.this.screen.blit(self.btn_save, (10, self.this.resolution_height-30))
        pass

class Main:
    def __init__(self, map):
        # 分辨率
        self.resolution = self.resolution_width, self.resolution_height = (1280, 720)
        # 屏幕对象
        self.screen = pygame.display.set_mode(self.resolution)
        
        pygame.init()
        # 窗口标题
        pygame.display.set_caption("MapGenerator - Nautical")
        # Logo
        pygame.display.set_icon(pygame.image.load(
            '_assets/logo.png').convert_alpha())
        #帧率
        self.clock = pygame.time.Clock()
        self.fps = 120
        # debug mode
        self.debug = False
        self.running = True
        
        self.components = components.Comp(self)
        self.router = "editor"
        self.map = map
        self.pointer_pos = (0, 0)
        
        self.editor = editor(self)
        self.actions = actions(self)
        self.generator = MapGenerator(self)
        self.sound = sound.BackgroundMusic(self)
        self.sound.editor_play()
        
        
    def run_loop(self):
        while self.running:
            self.generator.draw_action()
            self.actions.draw_action()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.components.onClick(event.pos)
                    self.generator.select_action(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    self.pointer_pos = event.pos
                if event.type == pygame.KEYDOWN:
                    # print(event.unicode)
                    if event.unicode in ["0","1","2","3","4"]:
                        self.generator.confirm_action(event.unicode)
                    if event.unicode == "5":
                        self.generator.setspawn()
                    
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()
        quit()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".json"):
            print("请直接输入地图编号 不需要带后缀")
            raise SystemExit
    main = Main(sys.argv[1] if len(sys.argv) > 1 else "0")
    main.run_loop()