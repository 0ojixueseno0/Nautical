import pygame

from pages.components import Card, Menu, PixelNum
from pages.components import Dialog

class Trade:
    def __init__(self, this):
        self.this = this
        self.background = pygame.transform.scale(
            pygame.image.load("_assets/trade/background.png")
            .convert_alpha(), (this.resolution_width, this.resolution_height)
        )
        
        self.menu = Menu(this,
                         yes_label="交易",
                         no_label="离开",
                         hint="点按库存内的卡片进行交易，点击交易按钮出售物品",
                         router="trade")
        
        self.villager = pygame.transform.scale(
            pygame.image.load("_assets/trade/villager.png")
            .convert_alpha(), (478, 285)
        )
        
        self.btn_buy = pygame.transform.scale(
            pygame.image.load("_assets/trade/btn_buy.png")
            .convert_alpha(), (62, 37)
        )
        self.btn_buy_rect = self.btn_buy.get_rect()
        self.btn_buy_rect.x = 311
        self.btn_buy_rect.y = 265
        this.Components.addComponent(self.btn_buy_rect, self.switch_window, router="trade", args="buy" )
        
        self.btn_sell = pygame.transform.scale(
            pygame.image.load("_assets/trade/btn_sell.png")
            .convert_alpha(), (62, 37)
        )
        self.btn_sell_rect = self.btn_sell.get_rect()
        self.btn_sell_rect.x = 413
        self.btn_sell_rect.y = 265
        this.Components.addComponent(self.btn_sell_rect, self.switch_window, router="trade", args="sell" )
        
        self.btn_supply = pygame.transform.scale(
            pygame.image.load("_assets/trade/btn_supply.png")
            .convert_alpha(), (136, 37)
        )
        self.btn_supply_rect = self.btn_supply.get_rect()
        self.btn_supply_rect.x = 338
        self.btn_supply_rect.y = 316
        this.Components.addComponent(self.btn_supply_rect, self.packsupply, router="trade")
        
        font = pygame.font.Font("_assets/pixelfont.ttf", 17)
        self.bobbletitle = font.render("选择交易类型", True, (255,255,255))
        
        self.this.showdialog = "buy"
        #* 商品卡片
        self.dialog_buy = TradeWindow(this, "购买货物")
        self.goods = [i for i in this.data.items[this.map:this.map + 4]]
        self.cards = [Card(this, i["icon"], i["name"]) for i in self.goods]
        self.cards_rect = [i.get_rect() for i in self.cards]
        
        for i, c in enumerate(self.cards_rect):
            c.x = self.cards_rect[i].x = 652 + (self.cards_rect[i].width + 47) * i
            c.y = self.cards_rect[i].y = 176
            this.Components.addComponent(
                c,
                self.select_goods,
                router="trade",
                isDialog=True,
                dialog_id = "buy",
                args=i
            )
        
        
        self.pixelnum = PixelNum(this)
        self.coin_icon = pygame.transform.scale(
            pygame.image.load("_assets/objects/coin.png")
            .convert_alpha(), (29,29)
        )
        
        self.sel_goods_bg = pygame.Surface(
            (self.cards_rect[0].width + 10, self.cards_rect[0].height + 45),
            pygame.SRCALPHA
        )
        self.sel_goods_bg.fill((114,83,52,128))
        # self.sel_goods_bg.fill((0,0,0,64))
        self.select_goods = None
        
        #* 收购卡片
        self.hint = font.render("请从库存中选择需要出售的货物", True, (255,255,255))
        self.hint_rect = self.hint.get_rect()
        self.dialog_sell = TradeWindow(this, "收购货物")
        self.rwarr = pygame.transform.scale(
            pygame.image.load("_assets/trade/rwarr.png")
            .convert_alpha(), (48,48)
        )
        self.select_item = None
    
    def packsupply(self):
        price = 5
        if self.this.player.supplies == 25:
            self.menu.change_hint("你已经补充完毕物资了，无需补充")
            return
        if self.this.player.money >= price:
            self.this.player.money -= price
            self.this.player.supplies = 25
            self.menu.upload_player_data()
        else:
            self.menu.change_hint("你的货币不足以补充物资")
            
            
            
    
    def switch_window(self, window:str):
        self.this.showdialog = window
    
    def select_goods(self, select):
        self.select_goods = select if self.select_goods != select else None
        pass
    
    def draw_action(self):
        self.this.screen.blit(self.background, (0, 0))
        self.menu.draw_action()
        self.this.screen.blit(self.villager, (33, 214))
        self.this.screen.blit(self.btn_buy, (311, 265))
        self.this.screen.blit(self.btn_sell, (413, 265))
        self.this.screen.blit(self.btn_supply, (325, 313))
        self.this.screen.blit(self.bobbletitle, (342, 235))
        
        if self.this.showdialog == "buy":
            self.dialog_buy.draw_action()
            if self.select_goods != None:
                self.this.screen.blit(self.sel_goods_bg, (
                    647 + (self.cards_rect[self.select_goods].width + 47) * self.select_goods,
                    171
                ))
            for i, c in enumerate(self.cards):
                c.draw_action((
                    652 + (self.cards_rect[i].width + 47) * i,
                    176,
                ))
                self.this.screen.blit(self.coin_icon, (
                    652 + (self.cards_rect[i].width + 47) * i,
                    300
                ))
                self.pixelnum.draw_action(
                    int(self.goods[i]["price"]),
                    (  
                        680 + (self.cards_rect[i].width + 47) * i,
                        300  
                    ),
                    (29,29)
                )
        elif self.this.showdialog == "sell":
            self.dialog_sell.draw_action()
            if self.select_item is None:
                self.this.screen.blit(self.hint, (533)) #TODO
            self.this.screen.blit(self.rwarr, (867,239))
        pass
        
        
class TradeWindow:
    def __init__(self, this, title: str):
        self.this = this
        self.background = pygame.transform.scale(
            pygame.image.load("_assets/trade/window.png")
            .convert_alpha(), (720, 240)
        )
        self.background_rect = self.background.get_rect()
        font = pygame.font.Font("_assets/pixelfont.ttf", 26)
        self.title = font.render(title, True, (255,255,255))
        self.title_rect = self.title.get_rect()
    
    
    def draw_action(self):
        self.this.screen.blit(self.background, (533, 124))
        self.this.screen.blit(self.title, (
            533 + (720 - self.title_rect.width) / 2,
            136))
        