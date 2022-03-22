import json
import os

class Data:
    def __init__(self):
        self.ships = []
        self.items = []
        self.events = []
        if self.check_file_exist():
            self.load_data()
        else:
            self.generate_file()
            self.load_data()
    
    def get_map_data(self, map: str):
        with open(f"_data/maps/{map}.json", encoding="utf-8") as f:
            return json.load(f)
    
    def check_file_exist(self):
        return os.path.exists("_data/ships.json") and os.path.exists("_data/items.json") and os.path.exists("_data/events.json")

    def generate_file(self):
        if not os.path.exists("_data"):
            os.mkdir("_data")
        open("_data/ships.json", "w").close() if not os.path.exists("_data/ships.json") else None
        open("_data/items.json", "w").close() if not os.path.exists("_data/items.json") else None
        open("_data/events.json", "w").close() if not os.path.exists("_data/events.json") else None
    
    def load_data(self):
        with open("_data/ships.json", encoding="utf-8") as f:
            self.ships = json.load(f)
        with open("_data/items.json", encoding="utf-8") as f:
            self.items = json.load(f)
        with open("_data/events.json", encoding="utf-8") as f:
            self.events = json.load(f)