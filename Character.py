class Character:
    def __init__(self, name, background_description):
        self.name = name
        self.actions = []
        self.appearance_modifiers = []
        self.background_description = background_description
        self.position = (0, 0)
        self.image = None

    def add_action(self, action):
        self.actions.append(action)

    def add_appearance_modifier(self, modifier):
        self.appearance_modifiers.append(modifier)

    def set_position(self, x, y):
        self.position = (x, y)

    def generate_image(self):
        # Image generation logic here
        pass
