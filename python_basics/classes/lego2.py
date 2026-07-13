class rocketdesgin:
    def __init__(self, colors, materials, fuel_capacity):
        self.colors = colors
        self.materials = materials
        self.fuel_capacity = fuel_capacity

    def describe(self):
        print(
            f"{self.colors}ロケットボディは{self.materials}できていて、燃料タンクの容量は{self.fuel_capacity}リットルです.")


degine1 = rocketdesgin("red", "alminum", "100000 liter")

degine1.describe()
