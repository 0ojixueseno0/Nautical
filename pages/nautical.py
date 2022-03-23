import pygame

from pages.components import Menu, Slot

class Nautical:
    def __init__(self, this):
        self.this = this
        
        self.background = pygame.transform.scale(
            pygame.image.load(f"_assets/maps/{this.map}.png"),
            (this.resolution_width*2, this.resolution_height*2)
        )
        self.background_rect = self.background.get_rect()
        
        self.mapdata = this.data.get_map_data(this.map)
        
        self.menu = Menu(this,
                        yes_label="航行",
                        no_label="停留",
                        btn_yes_func=self.sailing,
                        hint="点击高亮的航行点选择路线 点击航行按钮开始航行",
                        router="nautical")

        self.slot = Slot(this)
        self.prop = self.mapdata["map"]["prop"].split(":")
        self.coordinate()
        
        self.target_bg = pygame.Surface((10,10), pygame.SRCALPHA)
        self.target_bg.fill((255,0,0,128))
        
        self.selected_arr = pygame.transform.scale(
            pygame.image.load("_assets/objects/select.png")
            .convert_alpha(), (30,30)
        )
        self.selected_arr_rect = self.selected_arr.get_rect()
        
        self.ship_loc = [self.mapdata["spawn"]["x"],self.mapdata["spawn"]["y"]] # 船所在的坐标
        self.past_loc = [] # 走过的路径
        self.targets = [] # 可以行动的坐标组
        self.selected = [] # 选中的坐标
        
        
        self.ship_img = pygame.transform.scale(
            pygame.image.load(this.player.ship["icon"])
            .convert_alpha(), (self.coordinate_width, self.coordinate_height)
        )
        self.ship_rect = self.ship_img.get_rect()
        self.ship_pos = pygame.Vector2(self.parse_pos(self.ship_loc))
        # self.ship_pos = pygame.Vector2((0,0))
        self.offset = pygame.Vector2((0,0))
        # self.update_ship_loc()
        self.update_target()
    
    def update_target(self):
        targets = []
        x = self.ship_loc[0]
        y = self.ship_loc[1]
        for b in [x-1, x+1]:
            try:
                if self.mapdata["map"]["data"][y][b] != "0":
                    targets.append([b,y])
            except:
                continue
        for b in [y-1, y+1]:
            try:
                if self.mapdata["map"]["data"][b][x] != "0":
                    targets.append([x,b])
            except:
                continue
        try:
            targets.remove(self.past_loc)
        except:
            pass
        self.targets = targets
        # print(self.targets)
    
    def click_action(self, rawpos):
        rawpos = list(rawpos)
        rawpos[0] -= self.offset[0]
        rawpos[1] -= self.offset[1]
        rawpos = self.convert_pos(rawpos)
        if rawpos in self.targets:
            self.selected = [] if self.selected == rawpos else rawpos
    
    def sailing(self):
        if self.selected == []:
            self.menu.change_hint("请先选择航行点")
            return
        self.past_loc = self.ship_loc.copy()
        self.ship_loc = self.selected.copy()
        self.selected = []
        self.update_target()
        
    def update_ship_loc(self):
        # self.ship_rect.x = 
        # self.ship_rect.y = 
        ship_pos = pygame.Vector2(
            self.parse_pos(self.ship_loc)[0],
            self.parse_pos(self.ship_loc)[1]
        )
        self.ship_pos += (ship_pos - self.ship_pos) * 0.05
        self.ship_rect.x = self.ship_pos.x
        self.ship_rect.y = self.ship_pos.y
        offset = pygame.Vector2(
            -(self.ship_rect.center[0] - self.this.resolution_width//2),
            -(self.ship_rect.center[1] - self.this.resolution_height//2)
        )
        self.offset += (offset - self.offset) * 1
        self.offset.x = max(-(self.background_rect.width-self.this.resolution_width), min(0, self.offset.x))
        self.offset.y = max(-(self.background_rect.height-self.this.resolution_height), min(0, self.offset.y))
        
        
    def coordinate(self):
        self.coordinate_width = self.background_rect.width // int(self.prop[0])
        self.coordinate_height = self.background_rect.height // int(self.prop[1])
        pass
    
    def convert_pos(self, rawpos):
        x = int(rawpos[0] // self.coordinate_width)
        y = int(rawpos[1] // self.coordinate_height)
        return [x,y]
    
    def parse_pos(self, pos):
        x = pos[0] * self.coordinate_width
        y = pos[1] * self.coordinate_height
        return [x,y]
    
    # def select_action(self, rawpos):
    #     pos = self.convert_pos(rawpos)
    #     self.select = None if pos == self.select else pos
    
    def confirm_action(self, type):
        if self.select is not None:
            self.mapdata[self.select[1]][self.select[0]] = type
    
    def draw_action(self):
        self.this.screen.blit(self.background, self.offset)
        self.this.screen.blit(self.ship_img, self.ship_rect.move(self.offset))
        
        for i in self.targets:
            pos = self.parse_pos(i)
            self.this.screen.blit(self.target_bg, (
                pos[0] + self.offset[0] + self.coordinate_width//2 - 5,
                pos[1] + self.offset[1] + self.coordinate_height//2 - 5
            ))
        if self.selected != []:
            self.this.screen.blit(self.selected_arr, (
                self.offset[0] + self.parse_pos(self.selected)[0] + self.coordinate_width//2 - 16,
                self.offset[1] + self.parse_pos(self.selected)[1] + self.coordinate_height//2 - 40
            ))
        
        self.menu.draw_action()
        self.slot.draw_action()
        self.update_ship_loc()