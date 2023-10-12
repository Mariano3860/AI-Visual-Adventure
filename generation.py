# generation.py
from Background import Background
from Character import Character
from img_ai_helper import generate_character_image, generate_bg_image
from text_ai_helper import create_list_with_call_ai, create_object_with_call_ai, generate_bg_description


def create_characters(story, max_items):
    list_names = create_list_with_call_ai("names", max_items, story, 1)
    characters = []
    if list_names:
        print(list_names)
        print('List length:', len(list_names))
        characters = [Character(name) for name in list_names]
        characters = create_appearance_modifiers(characters, story)
        characters = create_actions(characters, story)
        characters = create_images(characters)
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


def create_images(characters):
    for character in characters:
        image = generate_character_image(character.get_description())
        if image:
            character.set_image(image)
    return characters


def create_background(story, width, height, story_length_description=300):
    bg_description = create_bg_description(story, story_length_description)
    if bg_description:
        bg = Background(bg_description, width, height)
    else:
        print("Background description couldn't be created")
        return None
    bg_img = create_bg_img(bg)
    if bg_img:
        bg.set_image(bg_img)
    return bg


def create_bg_description(story, length):
    bg_description = generate_bg_description(story, length, 1)
    if bg_description:
        return bg_description
    return None


def create_bg_img(bg):
    bg_img = generate_bg_image(bg.get_description(), bg.get_max_width(), bg.get_max_height())
    if bg_img:
        return bg_img
    return None
