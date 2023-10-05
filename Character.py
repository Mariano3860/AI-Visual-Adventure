# Character.py
class Character:
    def __init__(self, name, actions=None, appearance_modifiers=None,
                 background_description=None, position=(0, 0), image=None):
        self._name = name
        self._actions = actions if actions is not None else []
        self._appearance_modifiers = appearance_modifiers if appearance_modifiers is not None else []
        self._background_description = background_description if background_description is not None else []
        self._position = position
        self._image = image

    # Getter for name
    def get_name(self):
        return self._name

    # Setter for name
    def set_name(self, name):
        self._name = name

    # Getter for actions
    def get_actions(self):
        return self._actions

    # Add an action to the character
    def add_action(self, action):
        self._actions.append(action)

    # Getter for appearance modifiers
    def get_appearance_modifiers(self):
        return self._appearance_modifiers

    # Add an appearance modifier to the character
    def add_appearance_modifier(self, modifier):
        self._appearance_modifiers.append(modifier)

    # Getter for background description
    def get_background_description(self):
        return self._background_description

    # Setter for background description
    def set_background_description(self, description):
        self._background_description = description

    # Getter for position
    def get_position(self):
        return self._position

    # Setter for position
    def set_position(self, x, y):
        self._position = (x, y)

    def generate_image(self):
        # Image generation logic here
        pass

    # Getter for image
    def get_image(self):
        return self._image

    # Setter for image
    def set_image(self, image):
        self._image = image
