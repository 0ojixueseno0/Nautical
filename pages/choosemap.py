import pygame

from pages.components import Menu
from pages.components import Dialog
from pages.components import PixelNum
from pages.components import Card
class ChooseMap:
    def __init__(self, this):
        self.this = this
        
    def init(self):
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
        
        self.menu = Menu(this,
                         yes_label="选择",
                         no_label="返回",
                         hint="点击选择航行的地图",
                         router="choosemap",
                         btn_no_func=self.backtotitle,
                         btn_yes_func=self.go_nautical,
        )
        self.menu.set_ship_name()
        self.dialog = Dialog(this, "选择地图")
        self.num = PixelNum(this)
        self.x1 = 0
        self.x2 = self.x1 + self.cloudbg_copied_rect.width
        self.rollspeed = 0.2
        
        self.maps = [GameMap(self.this, "./_assets/choosemap/thumbnail_grey_{}.png".format(i), ["近贸","沿岸","远洋"][i]) for i in range(3)]
        self.maps_choosed = [GameMap(self.this, "./_assets/choosemap/thumbnail_{}.png".format(i), "") for i in range(3)]
        # self.maps = [Card(this, i["icon"], i["name"]) for i in range(3)]
        # self.cards.append(Card(this, "./_assets/objects/locked.png", " 敬请期待"))
        self.maps_rect = [i.get_rect() for i in self.maps]
        
        # self.offset = self.dialog.dialog_rect.width / pow(len(self.maps), 2) + self.maps_rect[0].width
        # self.map_pos = (self.dialog.dialog_rect.width /2 - self.maps_rect[0].width*len(self.maps)/2, 126)
        
        # self.shipinfo = shipinfo(this)
        
        for i, c in enumerate(self.maps_rect):
            c.x = self.maps_rect[i].x = 150 + i * (self.maps_rect[0].width + 10)
            c.y = self.maps_rect[i].y = 126
            this.Components.addComponent(
                c,
                self.choose_map,
                router="choosemap",
                args=i
            )
        self.selected = None
        
        self.pick_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/select.png")
            .convert_alpha(), (42,42)
        )
        self.pick_icon_rect = self.pick_icon.get_rect()
        
        
        # self.cardpos = [223, 166]
    def go_nautical(self):
        if self.selected is not None:
            self.this.map = self.selected
            self.this.player.inMap = True
            self.this.pages.darken_screen()
            self.this.router = "nautical"
            self.this.BackgroundMusic.startmenu_stop()
            self.this.pages.nautical.init(self.this)
            self.menu.delete()
            del(self.menu)
            self.this.BackgroundMusic.game_music_play()
            self.this.pages.nautical.on_first_round = True
        pass
    
    def choose_map(self, var):
        # print("choose ship:", ship)
        self.selected = var
    
    def backtotitle(self):
        self.this.pages.darken_screen()
        self.this.router = "startmenu"
        
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
        self.menu.draw_action()
        self.dialog.draw_action()
        # self.maps.draw_action()
        for i, c in enumerate(self.maps):
            c.draw_action((150 + i * (self.maps_rect[0].width + 10), 126))
        if self.selected is not None:
            for i, c in enumerate(self.maps_choosed):
                if i == self.selected:
                    c.draw_action((150 + i * (self.maps_rect[0].width + 10), 126))
            
        # if self.selected is not None:
        #     self.shipinfo.draw_action(
        #         self.this.data.ships[self.selected],
        #         (self.cards_rect[self.selected].x, self.cards_rect[self.selected].y + self.cards_rect[self.selected].height + 10)
        #     )
        # self.this.screen.blit(self.pick_icon, (self.card_pos[0] + self.selected * self.offset, self.card_pos[1] - self.pick_icon_rect.height))
class GameMap:
    def __init__(self, this, thumbnail=None ,label=None):
        self.this = this
        self.thumbnail = pygame.transform.scale(
            pygame.image.load("./_assets/choosemap/thumbnail_default.png" if thumbnail is None else thumbnail)
            .convert_alpha(), (320, 180)
        )
        self.thumbnail_rect = self.thumbnail.get_rect()
        font = pygame.font.Font("./_assets/pixelfont.ttf", 20)
        self.label = font.render("地图" if label is None else label, True, (255,255,255))
        self.label_rect = self.label.get_rect()
    
    def get_rect(self):
        self.thumbnail_rect.y += 34
        return self.thumbnail_rect
    
    def draw_action(self, pos=(0,0)):
        self.this.screen.blit(self.thumbnail, pos)
        self.this.screen.blit(self.label, (
            pos[0] + 160 - self.label_rect.width/2,
            pos[1] + 194
        ))