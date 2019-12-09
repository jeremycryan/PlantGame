import constants as c

class menu():
    def __init__(self, scene):
        self.scene = scene


class character_menu(menu):
    def __init__(self, scene):
        super().__init__(scene)
        self.text = ['Talk', 'Give', 'Quit']

class plant_menu(menu):
    def __init__(self, scene, growth_stage, plant_type, plot):
        super().__init__(scene)
        self.plot = plot
        self.plant_type = plant_type
        fruit_bearing = ['Strawberry']
        non_fruit_harvest = ['Jute', 'Moth Orchid']
        if growth_stage == c.DIRT:
            self.text = ['Plant Seed', 'Quit']
        if growth_stage == c.SEED:
            self.text = ['Remove Seed', 'Quit']
        elif growth_stage == c.SPROUT:
            self.text = ['Remove Plant', 'Quit']
        elif growth_stage == c.MATURE:
            if plant_type in non_fruit_harvest:
                self.text = ['Harvest', 'Prune', 'Remove Plant']
            else:
                self.text = ['Prune', 'Remove Plant']
        elif growth_stage == c.FRUIT:
            self.text = ['Harvest Fruit', 'Remove Plant']
