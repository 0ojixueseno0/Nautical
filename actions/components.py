import uuid
# print uuid.uuid1()
class Comp:
    def __init__(self, this):
        self.components = []
        self.this = this
        
    def clickCheck(self, pos, x, y, w, h) -> bool:
        return (x+w >= pos[0] >= x and y+h >= pos[1] >= y)
    
    def delComponent(self, cid):
        for i, c in enumerate(self.components):
            if c["id"] == cid:
                del(self.components[i])
                break
    
    def clear(self):
        self.components = []
    
    def addComponent(self, rect, function, router=None, args=None, isDialog=False, dialog_id=None):
        router = self.this.router if router is None else router
        comp = {
            "rect": rect,
            "func": function,
            "router": router,
            "args": args,
            "isinDialog": False,
            "id": str(uuid.uuid1())
        }
        if isDialog:
            comp["isinDialog"] = True
            comp["dialog_id"] = dialog_id
        self.components.append(comp)
        return comp["id"]
    
    def beforeAction(self, comp):
        if comp["isinDialog"]:
            return self.this.showdialog == comp["dialog_id"]
        if comp["router"] == "nautical":
            if self.this.pages.nautical.show_dialog and comp["isinDialog"] == False:
                return False
        return True
    
    def onClick(self, pos):
        for comp in self.components:
            if self.clickCheck(
                pos,
                comp["rect"].x,
                comp["rect"].y,
                comp["rect"].width,
                comp["rect"].height
                ) and comp["router"]==self.this.router:
                if self.beforeAction(comp):
                    print(comp["func"])
                    comp["func"](comp["args"]) if comp["args"] is not None else comp["func"]()