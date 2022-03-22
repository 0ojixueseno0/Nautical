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
        self.btn_sell = pygame.transform.scale(
            pygame.image.load("_assets/trade/btn_sell.png")
            .convert_alpha(), (62, 37)
        )
        font = pygame.font.Font("_assets/pixelfont.ttf", 17)
        self.bobbletitle = font.render("选择交易类型", True, (255,255,255))
        
        self.this.showdialog = "buy"
        #* 商品卡片
        self.dialog_buy = TradeWindow(this, "货物仓库")
        self.goods = [i for i in this.data.items[this.map:this.map + 4]]
        self.cards = [Card(this, i["icon"], i["name"]) for i in self.goods]
        self.cards_rect = [i.get_rect() for i in self.cards]
        
        self.this.components.addComponent()
        
        self.pixelnum = PixelNum(this)
        self.coin_icon = pygame.transform.scale(
            pygame.image.load("_assets/objects/coin.png")
            .convert_alpha(), (29,29)
        )
        
        self.sel_goods_bg = pygame.Surface(
            (self.cards_rect[0].width + 5, self.cards_rect[0].height + 40),
            pygame.SRCALPHA
        )
        self.sel_goods_bg.fill((0,0,0,128))
        
        self.select_goods = 0
    
    def select_goods(self, select):
        pass
    
    def draw_action(self):
        self.this.screen.blit(self.background, (0, 0))
        self.menu.draw_action()
        self.this.screen.blit(self.villager, (33, 214))
        self.this.screen.blit(self.btn_buy, (311, 290))
        self.this.screen.blit(self.btn_sell, (413, 290))
        self.this.screen.blit(self.bobbletitle, (342, 235))
        
        if self.this.showdialog == "buy":
            self.dialog_buy.draw_action()
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
        