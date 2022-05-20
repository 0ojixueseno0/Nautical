import random
import pygame

from pages.components import Dialog, Menu, Slot

class Nautical:
    def __init__(self, this):
        self.this = this
        self.on_first_round = True
        self.continue_game = False
        
    def init(self, this):
        self.show_dialog = False
        self.event_dialog = Dialog(this, title="事件")
        self.event_dialog_rect = self.event_dialog.get_rect()
        self.font = pygame.font.Font("_assets/pixelfont.ttf", 20)
        self.event_description = ""
        self.event_btn_label = self.font.render("好的", True, (0,0,0))
        self.event_btn_label_rect = self.event_btn_label.get_rect()
        self.event_btn = pygame.transform.scale(
            pygame.image.load("_assets/component/btn.png")
            .convert_alpha(), (124, 72)
        )
        self.event_btn_rect = self.event_btn.get_rect()
        self.event_btn_rect.x = this.resolution_width//2 - self.event_btn_rect.width//2 - 5
        self.event_btn_rect.y = self.event_dialog_rect.height - self.event_btn_rect.height
        this.Components.addComponent(self.event_btn_rect,
                                     self.close_dialog,
                                     router="nautical",
                                     isDialog=True,
                                     dialog_id="event_dialog")
        
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
                        btn_no_func=self.stay,
                        hint="点击航行点选择路线 点击航行按钮开始航行 双击航行点直接航行",
                        router="nautical")
        self.menu.set_ship_name()

        self.slot = Slot(this)
        self.prop = self.mapdata["map"]["prop"].split(":")
        self.coordinate()

        self.target_bg = {
            "up": pygame.transform.scale(
                pygame.image.load("_assets/nautical/g_arrow_up.png").convert_alpha(), (24,24)),
            "down": pygame.transform.scale(
                pygame.image.load("_assets/nautical/g_arrow_down.png").convert_alpha(), (24,24)),
            "left": pygame.transform.scale(
                pygame.image.load("_assets/nautical/g_arrow_left.png").convert_alpha(), (24,24)),
            "right": pygame.transform.scale(
                pygame.image.load("_assets/nautical/g_arrow_right.png").convert_alpha(), (24,24)),
        }
        # self.past_bg = {
        #     "down": pygame.transform.scale(
        #         pygame.image.load("_assets/nautical/r_arrow_up.png").convert_alpha(), (24,24)),
        #     "up": pygame.transform.scale(
        #         pygame.image.load("_assets/nautical/r_arrow_down.png").convert_alpha(), (24,24)),
        #     "right": pygame.transform.scale(
        #         pygame.image.load("_assets/nautical/r_arrow_left.png").convert_alpha(), (24,24)),
        #     "left": pygame.transform.scale(
        #         pygame.image.load("_assets/nautical/r_arrow_right.png").convert_alpha(), (24,24)),
        # }

        self.island_bg = pygame.transform.scale(
            pygame.image.load("_assets/nautical/island.png")
            .convert_alpha(), (24,24)
        )
        
        self.selected_arr = pygame.transform.scale(
            pygame.image.load("_assets/objects/select.png")
            .convert_alpha(), (30,30)
        )
        self.selected_arr_rect = self.selected_arr.get_rect()
        
        if self.continue_game == False:
            self.ship_loc = [self.mapdata["spawn"]["x"],self.mapdata["spawn"]["y"]] # 船所在的坐标
            self.past_loc = self.ship_loc # 走过的路径
            self.total_round = 0
        else:
            self.load_ship_data()
        self.targets = [] # 可以行动的坐标组
        self.islands = [] # 可以行动的岛屿组
        self.selected = [] # 选中的坐标
        
        self.round = this.player.ship["speed"] if this.player.hasShip else 0
        self.current_round = self.round
        # self.round_title = self.font.render("已航行了 {} 回合", True, (255,255,255))
        # self.round_title = 
        
        self.ship_img_left = pygame.transform.scale(
            pygame.image.load(this.player.ship["icon"])
            .convert_alpha(), (self.coordinate_width, self.coordinate_height)
        )
        self.ship_img_right = pygame.transform.flip(pygame.transform.scale(
            pygame.image.load(this.player.ship["icon"])
            .convert_alpha(), (self.coordinate_width, self.coordinate_height)
        ), True, False)
        
        self.ship_img = self.ship_img_left
        
        
        self.ship_rect = self.ship_img.get_rect()
        self.ship_pos = pygame.Vector2(self.parse_pos(self.ship_loc))
        # self.ship_pos = pygame.Vector2((0,0))
        self.offset = pygame.Vector2((0,0))
        # self.update_ship_loc()
        self.update_target()
        self.check_ship_loc()

    def load_ship_data(self):
        self.ship_loc = self.this.player.map["ship_loc"]
        self.past_loc = self.this.player.map["past_loc"]
        self.total_round = self.this.player.map["round"]
        self.check_ship_loc()
        self.show_target_dialog()
    
    def show_target_dialog(self):
        self.this.showdialog = "event_dialog"
        # self.event_dialog.change_title(event["name"])
        self.event_dialog.change_title("获胜目标")
        self.event_description = f"持有货币达到 {self.this.player.target_money} 金币"
        self.menu.change_hint(self.event_description)
        self.show_dialog = True

    
    def check_ship_loc(self):
        if self.this.player.rejoin:
            return
        block = self.mapdata["map"]["data"][self.ship_loc[1]][self.ship_loc[0]]
        if block in ["2","3","4"]:
            if block == "2":
                self.this.player.island = "A"
            elif block == "3":
                self.this.player.island = "B"
            elif block == "4":
                self.this.player.island = "C"
            self.this.pages.trade.load_data()
            self.this.pages.darken_screen()
            self.this.router = "trade"
            return True
        return False
    
    def random_bool(self, true:int=50) -> bool:
        # turenum: persent of true
        true = min(true, 100)
        return random.randint(0, 100) < true 

    def close_dialog(self):
        self.show_dialog = False
        self.on_first_round = False
        self.menu.change_hint("点击航行点选择路线 点击航行按钮开始航行 双击航行点直接航行")
        self.this.showdialog = ""
        self.this.player.check_win_lose()

    def run_event(self, event):
        eid = event["eid"]
        print("Event:",eid)
        if eid == "nothing_happened":
            self.menu.change_hint(event["description"])
            return
        if eid == "fix_ship":
            self.menu.change_hint(
                event["description"] 
                if self.this.player.ship["durable"] < self.this.player.ship["max_durable"] 
                else event["description_fail"]
            )
            self.this.player.ship["durable"] += 1 if self.this.player.ship["durable"] < self.this.player.ship["max_durable"] else 0
            return
        self.this.showdialog = "event_dialog"
        self.event_dialog.change_title(event["name"])
        self.event_description = event["description"]
        if eid == "get_random_item":
            if self.this.player.ship["capacity"] - len(self.this.player.inventory) > 0:
                item = random.choice(self.this.data.items)
                self.this.player.inventory.append(item)
                self.slot.generate_cards()
                self.event_description = self.event_description.format(item["name"])
            else:
                self.event_description = event["fail"]
        elif eid == "add_speed":
            self.round += random.randint(1,5)
        elif eid == "fishing":
            addsupply = random.randint(1,5)
            self.event_description = self.event_description.format(addsupply)
            self.this.player.supplies += addsupply
        elif eid == "pirate_attack":
            self.this.BackgroundMusic.play_piracy()
            if len(self.this.player.inventory) > 0:
                item = random.randint(0,len(self.this.player.inventory)-1)
                self.event_description = event["description"].format(self.this.player.inventory[item]["name"])
                del(self.this.player.inventory[item])
                self.slot.generate_cards()
            else:
                self.event_description = event["fail"]
                self.this.player.ship["durable"] -= 1
                if self.this.player.money > 1:
                    self.event_description += " 抢走了你的金币"
                    self.this.player.money -= random.randint(1,self.this.player.money//2)
        elif eid == "random_damage":
            if self.this.player.ship["durable"] > 2:
                self.this.player.ship["durable"] -= random.randint(1,2)
            else:    
                self.this.player.ship["durable"] -= 1
            pass
        self.menu.change_hint(self.event_description)
        self.show_dialog = True
        pass
    
    def events(self):
        danger = self.this.player.ship["danger"]
        danger *= 5
        normal = 100 - danger
        luck = random.randint(0,100)
        print("Danger:",danger,"Normal:",normal,"Luck:",luck)
        if luck > normal:
            event = random.randint(0,len(self.this.data.events["good_events"])-1)
            self.run_event(self.this.data.events["good_events"][event])
            pass
        elif danger <= luck <= normal:
            event = random.randint(0,len(self.this.data.events["normal_events"])-1)
            self.run_event(self.this.data.events["normal_events"][event])
            pass
        elif luck < danger:
            event = random.randint(0,len(self.this.data.events["bad_events"])-1)
            self.run_event(self.this.data.events["bad_events"][event])
            pass
    
    
    def stay(self):
        if self.check_round():
            if self.random_bool(100):
                self.events()
            pass
    
    def check_round(self):
        if self.current_round == 0:
            self.current_round = self.round
            self.total_round += 1
            self.this.player.supplies -= 1
            if self.this.player.check_win_lose():
                return False
            if self.random_bool():
                self.events()
        else:
            self.current_round -= 1
        return True
    
    def update_target(self):
        targets = []
        islands = []
        x = self.ship_loc[0]
        y = self.ship_loc[1]
        for b in [x-1, x+1]:
            try:
                if self.mapdata["map"]["data"][y][b] != "0":
                    if self.mapdata["map"]["data"][y][b] == "1":
                        targets.append([b,y])
                    else:
                        islands.append([b,y])
            except:
                continue
        for b in [y-1, y+1]:
            try:
                if self.mapdata["map"]["data"][b][x] != "0":
                    if self.mapdata["map"]["data"][b][x] == "1":
                        targets.append([x,b])
                    else:
                        islands.append([x,b])
            except:
                continue
        try:
            islands.remove(self.past_loc)
        except:
            pass
        try:
            targets.remove(self.past_loc)
        except:
            pass
        self.targets = targets
        self.islands = islands
        # print(self.targets)
    
    def click_action(self, rawpos):
        rawpos = list(rawpos)
        rawpos[0] -= self.offset[0]
        rawpos[1] -= self.offset[1]
        rawpos = self.convert_pos(rawpos)
        if rawpos in self.targets or rawpos in self.islands:
            if self.selected == rawpos:
                self.sailing()
            else:
                self.selected = rawpos
    
    def sailing(self):
        if self.selected == []:
            self.menu.change_hint("请先选择航行点")
            return
        if self.this.player.rejoin:
            self.this.player.rejoin = False
        self.past_loc = self.ship_loc.copy()
        self.ship_loc = self.selected.copy()
        if self.parse_direct(self.past_loc) == "right":
            self.ship_img = self.ship_img_left
        elif self.parse_direct(self.past_loc) == "left":
            self.ship_img = self.ship_img_right
        self.selected = []
        self.menu.change_hint("点击航行点选择路线 点击航行按钮开始航行 双击航行点直接航行")
        self.update_target()
        if self.check_ship_loc():
            return
        self.check_round()
        
    def update_ship_loc(self):
        # self.ship_rect.x = 
        # self.ship_rect.y = 
        ship_pos = pygame.Vector2(
            self.parse_pos(self.ship_loc)[0],
            self.parse_pos(self.ship_loc)[1]
        )
        self.ship_pos += (ship_pos - self.ship_pos) * 0.1
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
    
    def parse_direct(self, pos):
        if self.ship_loc[0] < pos[0]:
            return "right"
        elif self.ship_loc[0] > pos[0]:
            return "left"
        elif self.ship_loc[1] < pos[1]:
            return "down"
        elif self.ship_loc[1] > pos[1]:
            return "up"
        else:
            return "stay"
    
    def draw_action(self):
        self.this.screen.blit(self.background, self.offset)
        self.this.screen.blit(self.ship_img, self.ship_rect.move(self.offset))
        
        for i in self.targets:
            direct = self.parse_direct(i)
            pos = self.parse_pos(i)
            self.this.screen.blit(self.target_bg[direct], (
                pos[0] + self.offset[0] + self.coordinate_width//2 - 10,
                pos[1] + self.offset[1] + self.coordinate_height//2 - 8
            ))
        # direct = self.parse_direct(self.past_loc)
        # pos = self.parse_pos(self.past_loc)
        # self.this.screen.blit(self.past_bg[direct], (
        #     pos[0] + self.offset[0] + self.coordinate_width//2 - 10,
        #     pos[1] + self.offset[1] + self.coordinate_height//2 - 8
        # ))
        if self.selected != []:
            self.this.screen.blit(self.selected_arr, (
                self.offset[0] + self.parse_pos(self.selected)[0] + self.coordinate_width//2 - 16,
                self.offset[1] + self.parse_pos(self.selected)[1] + self.coordinate_height//2 - 40
            ))
        for i in self.islands:
            pos = self.parse_pos(i)
            self.this.screen.blit(self.island_bg, (
                pos[0] + self.offset[0] + self.coordinate_width//2 - 12,
                pos[1] + self.offset[1] + self.coordinate_height//2 - 12
            ))
        if self.selected != []:
            self.this.screen.blit(self.selected_arr, (
                self.offset[0] + self.parse_pos(self.selected)[0] + self.coordinate_width//2 - 16,
                self.offset[1] + self.parse_pos(self.selected)[1] + self.coordinate_height//2 - 40
            ))
        
        self.menu.draw_action()
        self.slot.draw_action()
        
        #dialog
        if self.show_dialog:
            self.event_dialog.draw_action()
            self.this.screen.blit(self.event_btn, (
                self.this.resolution_width//2 - self.event_btn_rect.width//2 - 5,
                self.event_dialog_rect.height - self.event_btn_rect.height
            ))
            self.this.screen.blit(self.event_btn_label, (
                self.this.resolution_width//2 - self.event_btn_label_rect.width//2 - 5,
                self.event_dialog_rect.height - self.event_btn_label_rect.height - self.event_btn_label_rect.height - 5
            ))
            desc = self.font.render(self.event_description, True, (255,255,255))
            desc_rect = desc.get_rect()
            self.this.screen.blit(desc, (
                self.this.resolution_width//2 - desc_rect.width//2,
                self.event_dialog_rect.height//2 - desc_rect.height//2 + 20
            ))
        
        total_round = self.font.render("已航行了 {} 回合".format(self.total_round), True, (255,255,255))
        total_round_rect = total_round.get_rect()
        self.this.screen.blit(total_round, (
            self.this.resolution_width - total_round_rect.width - 5,
            5
        ))
        
        self.update_ship_loc()