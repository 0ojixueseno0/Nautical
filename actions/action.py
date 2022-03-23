
class MainActions:
    def __init__(self, this):
        self.this = this
    def action(self):
        if self.this.router == "startmenu":
            self.this.pages.startpage.rollbg_action()
        elif self.this.router == "wharf":
            self.this.pages.wharf.rollbg_action()

class DrawActions:
    def __init__(self, this):
        self.this = this
    def action(self):
        if self.this.router == "startmenu":
            self.this.pages.startpage.draw_action()
        elif self.this.router == "wharf":
            self.this.pages.wharf.draw_action()
        elif self.this.router == "trade":
            self.this.pages.trade.draw_action()
        elif self.this.router == "nautical":
            self.this.pages.nautical.draw_action()
        