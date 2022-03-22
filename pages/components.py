# 页面通用组件将在此显示

import pygame

class Menu:
    def __init__(self, this, yes_label="确定", no_label="取消", hint="这是默认的提示信息", btn_yes_func=None, btn_no_func=None, router=None):
        self.this = this
        self.surface = pygame.Surface((1280,222), pygame.SRCALPHA)
        self.surface.fill((0,0,0,135))
        self.logo = pygame.transform.scale(
            pygame.image.load("./_assets/component/menu.png")
            .convert_alpha(), (121, 49)
        )
        self.logo_rect = self.logo.get_rect()
        
        self.slot = pygame.transform.scale(
            pygame.image.load("./_assets/component/slot.png")
            .convert_alpha(), (470, 100)
        )
        self.slot_rect = self.slot.get_rect()
        
        self.font = pygame.font.Font("./_assets/pixelfont.ttf", 20)
        self.slot_title = self.font.render("库存", True, (255,255,255))
        self.btn_yes_label = self.font.render(yes_label, True, (0,0,0))
        self.btn_no_label = self.font.render(no_label, True, (0,0,0))
        
        self.font = pygame.font.Font("./_assets/pixelfont.ttf", 17)
        self.hint = self.font.render(hint, True, (255,255,255))
        self.hint_rect = self.hint.get_rect()
        
        self.btn_yes = self.btn_no = pygame.transform.scale(
            pygame.image.load("./_assets/component/btn.png")
            .convert_alpha(), (90, 52)
        )
        self.btn_yes_rect = self.btn_yes.get_rect()
        self.btn_yes_rect.x, self.btn_yes_rect.y = 902, 611
        self.btn_no_rect = self.btn_no.get_rect()
        self.btn_no_rect.x, self.btn_no_rect.y = 1063, 611
        this.Components.addComponent(
            self.btn_yes_rect,
            self.btn_yes_action if btn_yes_func is None else btn_yes_func, 
            this.router if router is None else router)
        this.Components.addComponent(
            self.btn_no_rect, 
            self.btn_no_action if btn_no_func is None else btn_no_func, 
            this.router if router is None else router)
        self.money_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/coin.png")
            .convert_alpha(), (29,29)
        )
        self.supplies_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/supplies.png")
            .convert_alpha(), (29,29)
        )
        self.ship_icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/locked.png")
            .convert_alpha(), (30,30)
        )
        self.ship_durable = pygame.transform.scale(
            pygame.image.load("./_assets/wharf/durable.png")
            .convert_alpha(), (27,27)
        )
        if this.player.hasShip:
            self.ship_name = self.font.render(this.player.ship["name"], True, (255,255,255))
            self.player_supplies = int(this.player.supplies)
            self.durable = int(this.player.ship["durable"])
        self.player_money = int(this.player.money)
        self.pixnum = PixelNum(this)
    
    def upload_player_data(self):
        if self.this.player.hasShip:
            self.player_supplies = int(self.this.player.supplies)
            self.durable = int(self.this.player.ship["durable"])
        self.player_money = int(self.this.player.money)
    
    def change_hint(self, hint: str):
        self.hint = self.font.render(hint, True, (255,255,255))
        self.hint_rect = self.hint.get_rect()
    
    def btn_yes_action(self):
        print("Menu: default btn yes")
    
    def btn_no_action(self):
        print("Menu: default btn no")
        
    def draw_action(self):
        self.this.screen.blit(self.surface, (0, 499))
        self.this.screen.blit(self.logo, (40, 515))
        self.this.screen.blit(self.slot, (36, 597))
        self.this.screen.blit(self.slot_title, (58, 571))
        self.this.screen.blit(self.hint, (
            self.this.resolution_width - self.hint_rect.width - 10,
            self.this.resolution_height - self.hint_rect.height - 10
        ))
        self.this.screen.blit(self.btn_yes, (self.btn_yes_rect.x, self.btn_yes_rect.y))
        self.this.screen.blit(self.btn_no, (self.btn_no_rect.x, self.btn_no_rect.y))
        self.this.screen.blit(self.btn_yes_label, (self.btn_yes_rect.x + 25, self.btn_yes_rect.y + 16))
        self.this.screen.blit(self.btn_no_label, (self.btn_no_rect.x + 25, self.btn_no_rect.y + 16))
        if self.this.player.hasShip:
            self.this.screen.blit(self.ship_icon, (567, 577)) #Ship 1
            self.this.screen.blit(self.ship_name, (605, 585))
            
            self.this.screen.blit(self.supplies_icon, (567, 643)) #Supply 3
            self.pixnum.draw_action(self.player_supplies, (597, 643), (29,29))
            
            self.this.screen.blit(self.ship_durable, (569, 674)) #Durable 4
            self.pixnum.draw_action(self.durable, (597, 674), (29,29))
        self.this.screen.blit(self.money_icon, (567, 612)) #Money 2
        self.pixnum.draw_action(self.player_money,(597, 612), (29,29))
class Dialog:
    def __init__(self, this, title:str):
        self.this = this
        font = pygame.font.Font("./_assets/pixelfont.ttf", 33)
        self.title = font.render(title, True, (255,255,255))
        self.title_rect = self.title.get_rect()
        self.dialog = pygame.transform.scale(
            pygame.image.load("./_assets/component/dialog.png")
            .convert_alpha(), (1140, 400)
        )
        self.dialog_rect = self.dialog.get_rect()
        self.dialog_rect.x, self.dialog_rect.y = 70, 49
    
    def draw_action(self, pos=(70, 49)):
        self.this.screen.blit(self.dialog, pos)
        self.this.screen.blit(self.title, (
            self.this.resolution_width/2 - self.title_rect.width/2,69
        ))

class PixelNum:
    def __init__(self, this):
        self.this = this
        self.num = [pygame.image.load(f"./_assets/component/{i}.png").convert_alpha() for i in range(10)]
        self.num.extend([
            pygame.image.load("./_assets/component/dot.png").convert_alpha(),
            pygame.image.load("./_assets/component/e.png").convert_alpha(),
        ])
        self.num_rect = [i.get_rect() for i in self.num]
    
    def draw_action(self, num:int, pos:tuple, size:tuple=(40,40)):
        offset = 0
        for i in str(num):
            if i in ["+","-"]: continue
            i = 11 if i=="e" else i
            i = 10 if i=="." else int(i)
            self.this.screen.blit(
                pygame.transform.scale(self.num[i], size),
                (pos[0] + offset, pos[1])
            )
            self.num_rect[i].width = size[0]*1.1
            offset += self.num_rect[i].width/2

class Card:
    def __init__(self, this, icon=None, label=None, small=False):
        self.this = this
        self.small = small
        self.icon = pygame.transform.scale(
            pygame.image.load("./_assets/objects/default.png" if icon is None else icon)
            .convert_alpha(), (35,35) if small else (60, 60)
        )
        self.icon_rect = self.icon.get_rect()
        self.cardbg = pygame.transform.scale(
            pygame.image.load("./_assets/component/card.png")
            .convert_alpha(), (65, 88) if small else (85, 116)
        )
        self.cardbg_rect = self.cardbg.get_rect()
        font = pygame.font.Font("./_assets/pixelfont.ttf", 13 if small else 15)
        self.label = font.render("包裹" if label is None else label, True, (0,0,0))
        self.label_rect = self.label.get_rect()
    
    def get_rect(self):
        return self.cardbg_rect
    
    def draw_action(self, pos=(0,0)):
        self.this.screen.blit(self.cardbg, (pos[0], pos[1]))
        self.this.screen.blit(
            self.icon,
            (
                pos[0] + 15 if self.small else pos[0] + 12, 
                pos[1] + 20 if self.small else pos[1] + 15
            )
        )
        self.this.screen.blit(
            self.label,
            (
                pos[0] + self.cardbg_rect.width/2 - self.label_rect.width/2,
                pos[1] + self.cardbg_rect.height - self.label_rect.height - 15
            )
        )
        pass