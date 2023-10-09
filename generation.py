# generation.py
from Character import Character
from text_ai_helper import create_list_with_call_ai, create_object_with_call_ai


def create_characters(story, max_items):
    list_names = create_list_with_call_ai("names", max_items, story, 1)
    characters = []
    if list_names:
        print(list_names)
        print('List length:', len(list_names))
        characters = [Character(name) for name in list_names]
        characters = create_appearance_modifiers(characters, story)
        characters = create_actions(characters, story)
    return characters


def create_appearance_modifiers(characters, story):
    object_names_adjective = create_object_with_call_ai(
        "adjective", [character.get_name() for character in characters], story, 1, 2)
    if object_names_adjective:
        print(object_names_adjective)
        for character in characters:
            name = character.get_name()
            if name in object_names_adjective:
                character.add_appearance_modifier(object_names_adjective[name])
    return characters


def create_actions(characters, story):
    object_names_actions = create_object_with_call_ai(
        "actions", [character.get_name() for character in characters], story, 1, 1)
    if object_names_actions:
        print(object_names_actions)
        for character in characters:
            name = character.get_name()
            if name in object_names_actions:
                character.add_action(object_names_actions[name])
    return characters