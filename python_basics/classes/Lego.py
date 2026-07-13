class LegoBuilding:

    def __init__(self, color, floors, doors, windows):
        self.color = color
        self.floors = floors
        self.doors = doors
        self.windows = windows

    def describe(self):
        print(
            f"{self.color}の{self.floors}階建て,"
            f"床{self.doors},"
            f"窓{self.windows},"

            f"のLEGOハウスです."
        )


house1 = LegoBuilding("赤", 2, 'glass', "gold",)
house2 = LegoBuilding("緑", 4, "glass", "silver",)

house1.describe()
house2.describe()
