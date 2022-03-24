import json

class Player:
    def __init__(self, this):
        self.this = this
        self.init()
    
    def init(self):
        with open("./_data/player.json", encoding="utf-8") as f:
            data = json.load(f)
        self.money = data["money"]
        self.target_money = 2 * self.money
        self.supplies = data["supplies"]
        self.ship = data["ship"]
        self.inventory = data["inventory"]
        self.hasShip = False
        self.location = "A" # 所在岛屿
    
    def clear(self):
        self.money = max(25, self.money)
        self.supplies = 0
        del(self.ship)
        self.ship = {}
        del(self.inventory)
        self.inventory = []
        self.save_player()
    
    def check_win_lose(self):
        if self.money >= self.target_money:
            self.this.gameover_reason = f"你胜利了！你的资产达到了 {int(self.money)}/{self.target_money} 金币"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
        if self.supplies <= 0:
            self.this.gameover_reason = f"你失败了！你的物资不够航行了"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
        if self.ship["durable"] <= 0:
            self.this.gameover_reason = f"你失败了！你的船只被摧毁了"
            self.this.pages.win_lose.init()
            self.this.pages.darken_screen()
            self.this.router = "win_lose"
    
    def reset_player(self):
        data = {
            "money": 25,
            "supplies": 0,
            "ship": {},
            "inventory": []
        }
        with open("./_data/player.json", "w") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    def save_player(self):
        data = {
            "money": self.money,
            "supplies": self.supplies,
            "ship": self.ship,
            "inventory": self.inventory
        }
        with open("./_data/player.json", "w") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            