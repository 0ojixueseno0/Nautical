import json
import atexit

class Player:
    def __init__(self, this):
        self.this = this
        self.init()
        atexit.register(self.exit_debug)
        
    def init(self):
        with open("./_data/player.json", encoding="utf-8") as f:
            data = json.load(f)
        self.money = data["money"]
        self.target_money = data["target_money"]
        self.supplies = data["supplies"]
        self.ship = data["ship"]
        self.inventory = data["inventory"]
        self.hasShip = data["hasShip"]
        self.island = "A" # 所在岛屿
        self.inMap = data["inMap"]
        self.map = data["map"]
        self.rejoin = data["rejoin"] if self.inMap else False
    
    def clear(self):
        self.money = max(25, self.money)
        self.target_money = 2 * self.money
        self.supplies = 0
        self.hasShip = False
        self.rejoin = False
        del(self.ship)
        self.ship = {}
        del(self.inventory)
        self.inventory = []
        self.inMap = False
        del(self.map)
        self.map = {}
        self.save_player()
    
    def check_win_lose(self):
        if self.money >= self.target_money:
            self.this.gameover_reason = f"你胜利了！你的资产达到了 {int(self.money)}/{self.target_money} 金币"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
            return True
        if self.supplies <= 0:
            self.this.gameover_reason = f"你失败了！你的物资不够航行了"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
            return True
        if self.ship["durable"] <= 0:
            self.this.gameover_reason = f"你失败了！你的船只被摧毁了"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
            return True
    
    def reset_player(self):
        self.clear()
        data = {
            "money": 25 if self.money < 25 else self.money,
            "target_money": 2 * self.money,
            "rejoin": False,
            "supplies": 0,
            "hasShip": False,
            "ship": {},
            "inventory": [],
            "inMap": False,
            "map": {}
        }
        with open("./_data/player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    def exit_debug(self):
        self.rejoin = True
        self.save_player()
    
    def save_player(self):
        try:
            mapid = self.this.map
            shiploc = self.this.pages.nautical.ship_loc
            pastloc = self.this.pages.nautical.past_loc
            gameround = self.this.pages.nautical.total_round
        except AttributeError:
            try:
                shiploc = self.map["ship_loc"]
                pastloc = self.map["past_loc"]
                gameround =  self.map["round"]
                mapid = self.map["mapid"]
            except:
                shiploc = None
                pastloc = None
                gameround = None

        data = {
            "money": self.money,
            "target_money": self.target_money,
            "rejoin": self.rejoin,
            "supplies": self.supplies,
            "hasShip": self.hasShip,
            "ship": self.ship,
            "inventory": self.inventory,
            "inMap": self.inMap,
            "map": {
                "mapid": mapid,
                "ship_loc": shiploc,
                "past_loc": pastloc,
                "round": gameround
            }
        }
        with open("./_data/player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            