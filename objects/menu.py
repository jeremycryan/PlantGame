import constants as c

class menu():
    def __init__(self, scene):
        self.scene = scene
        self.text = []


class character_menu():
    def __init__(scene, self):
        super().__init__(scene)
        self.text = ['Talk', 'Give', 'Quit']

class plant_menu():
    def __init__(self, scene, growth_stage, plant_type):
        super().__init__(scene)
        self.plant_type = plant_type
        self.text = []
        if growth_stage == c.DIRT:
            self.text = ['Plant Seed', 'Quit']
        if growth_stage == c.SEED:
            self.text = ['Remove Seed', 'Quit']
        elif growth_stage == c.SPROUT:
            self.text = ['Remove Plant', 'Quit']
        elif growth_stage == c.MATURE:
            self.text = ['Prune', 'Remove Plant']
        elif growth_stage == c.FRUIT:
            self.text = ['Harvest Fruit', 'Remove Plant']
