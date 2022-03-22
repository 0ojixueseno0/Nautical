import json

class Player:
    def __init__(self, this):
        self.this = this
        with open("./_data/player.json", encoding="utf-8") as f:
            data = json.load(f)
        self.money = data["money"]
        self.supplies = data["supplies"]
        self.ship = data["ship"]
        self.inventory = data["inventory"]
        self.hasShip = True
        self.location = "A"
    
    
    def reset_player(self):
        data = {
            "money": 10,
            "supplies": 0,
            "ship": {},
            "inventory": []
        }
        with open("./_data/player.json") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    def save_player(self):
        data = {
            "money": self.money,
            "supplies": self.supplies,
            "ship": self.ship,
            "inventory": self.inventory
        }
        with open("./_data/player.json") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            