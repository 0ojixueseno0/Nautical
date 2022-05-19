import turtle
import pygame

from pages.components import Menu
from pages.components import Dialog
from pages.components import PixelNum
from pages.components import Card
class Wharf:
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
                         yes_label="购买",
                         no_label="返回",
                         hint="使用初始资金购买需要出海航行的船只",
                         router="wharf",
                         btn_no_func=self.backtotitle,
                         btn_yes_func=self.buy_ship,
        )
        self.dialog = Dialog(this, "造船厂")
        self.num = PixelNum(this)
        self.x1 = 0
        self.x2 = self.x1 + self.cloudbg_copied_rect.width
        self.rollspeed = 0.2
        
        self.cards = [Card(this, i["icon"], i["name"]) for i in this.data.ships]
        self.cards.append(Card(this, "./_assets/objects/locked.png", " 敬请期待"))
        self.cards_rect = [i.get_rect() for i in self.cards]
        
        self.offset = self.dialog.dialog_rect.width / pow(len(self.cards), 2) + self.cards_rect[0].width
        self.card_pos = (self.dialog.dialog_rect.width /2 - self.cards_rect[0].width*len(self.cards)/2, 166)
        
        self.shipinfo = shipinfo(this)
        
        for i, c in enumerate(self.cards_rect):
            if i == len(self.cards_rect) - 1:
                break
            c.x = self.cards_rect[i].x = self.card_pos[0] + i * self.offset
            c.y = self.cards_rect[i].y = self.card_pos[1]
            this.Components.addComponent(
                c,
                self.choose_ship,
                router="wharf",
                args=i
            )
        self.selected = None
        
        self.pick_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/select.png")
            .convert_alpha(), (42,42)
        )
        self.pick_icon_rect = self.pick_icon.get_rect()
        
        
        # self.cardpos = [223, 166]
    def buy_ship(self):
        if self.this.data.ships[self.selected]["price"] <= self.this.player.money and self.selected is not None:
            self.this.pages.darken_screen()
            self.this.player.money -= self.this.data.ships[self.selected]["price"]
            self.this.player.ship = self.this.data.ships[self.selected].copy()
            self.this.player.supplies = 15
            self.this.player.hasShip = True
            self.this.router = "choosemap"
            # self.this.BackgroundMusic.startmenu_stop()
            self.this.pages.choosemap.init()
            self.menu.delete()
            del(self.menu)
            # pygame.time.delay(200)
            # self.this.BackgroundMusic.game_music_play()
            # self.this.pages.nautical.target_dialog()
            # self.this.pages.nautical.on_first_round = True
        pass
    
    def choose_ship(self, ship):
        # print("choose ship:", ship)
        self.selected = ship
        if self.this.data.ships[self.selected]["price"] > self.this.player.money:
            self.menu.change_hint("你的资金不足以购买该船只")
        else:
            self.menu.change_hint("点击购买按钮购买该船只")
    
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
        for i, c in enumerate(self.cards):
            c.draw_action((self.card_pos[0] + i * self.offset, self.card_pos[1]))
        if self.selected is not None:
            self.this.screen.blit(self.pick_icon, (
                self.cards_rect[self.selected].x + self.cards_rect[self.selected].width / 2 - self.pick_icon_rect.width / 2,
                self.cards_rect[self.selected].y - self.pick_icon_rect.height)
            )
        if self.selected is not None:
            self.shipinfo.draw_action(
                self.this.data.ships[self.selected],
                (self.cards_rect[self.selected].x, self.cards_rect[self.selected].y + self.cards_rect[self.selected].height + 10)
            )
        # self.this.screen.blit(self.pick_icon, (self.card_pos[0] + self.selected * self.offset, self.card_pos[1] - self.pick_icon_rect.height))

class shipinfo:
    def __init__(self, this):
        self.this = this
        font = pygame.font.Font("./_assets/pixelfont.ttf", 18)
        self.label = [
            font.render("容量", True, (255,255,255)),
            font.render("速度", True, (255,255,255)),
            font.render("耐久", True, (255,255,255)),
            font.render("售价", True, (255,255,255)),
        ]
        self.label_rect = [i.get_rect() for i in self.label]
        
        self.capacoty_icon = pygame.transform.scale(
            pygame.image.load("./_assets/wharf/capacoty.png")
            .convert_alpha(), (24,24)
        )
        self.icon_rect = self.capacoty_icon.get_rect()
        
        self.durable_icon = pygame.transform.scale(
            pygame.image.load("./_assets/wharf/durable.png")
            .convert_alpha(), (24,24)
        )
        self.speed_icons = [pygame.transform.scale(
            pygame.image.load(f"./_assets/wharf/speed{i}.png")
            .convert_alpha(), (24,24)
        ) for i in range(3)]
        self.coin_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/coin.png")
            .convert_alpha(), (24,24)
        )
        self.price_icon = PixelNum(this)
    
    def draw_action(self, ship:dict, pos:turtle=(0,0)):
        for i, label in enumerate(self.label):
            self.this.screen.blit(label, (pos[0], pos[1] + i * 30))
        for e in range(ship["capacity"]):
            self.this.screen.blit(self.capacoty_icon, (pos[0] + self.label_rect[0].width + 5 + e * 25, pos[1]))
        for e in range(ship["speed"]):
            if ship["speed"] < 3:
                self.this.screen.blit(
                    self.speed_icons[0],
                    (pos[0] + self.label_rect[1].width + 5 + e * 25,
                     pos[1] + 30))
            elif 3 <= ship["speed"] < 6:
                self.this.screen.blit(
                    self.speed_icons[1],
                    (pos[0] + self.label_rect[1].width + 5 + e * 25,
                     pos[1] + 30))
            else:
                self.this.screen.blit(
                    self.speed_icons[2],
                    (pos[0] + self.label_rect[1].width + 5 + e * 25, 
                     pos[1] + 30))
        for e in range(ship["durable"]):
            self.this.screen.blit(self.durable_icon, (pos[0] + self.label_rect[2].width + 5 + e * 25, pos[1] + 60))
        self.this.screen.blit(self.coin_icon, (pos[0] +  self.label_rect[-1].width + 5, pos[1] + 90))
        self.price_icon.draw_action(ship["price"], (pos[0] + self.label_rect[-1].width + 25, pos[1] + 90), size=(24,24))
        pass