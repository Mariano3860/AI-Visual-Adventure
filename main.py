from Character import Character
from ai_helper import create_list_with_call_ai, create_object_with_call_ai

if __name__ == '__main__':
    characters = []
    story = "Game of thrones"
    max_items = 30
    item_type = "names"
    list_names = create_list_with_call_ai(item_type, max_items, story, 1)

    if list_names and len(list_names) > 0:
        print(list_names)
        print('List length: ' + str(len(list_names)))
        characters = [Character(name) for name in list_names]

        item_type = "adjective"
        max_attrib = 2
        object_names_adjective = create_object_with_call_ai(item_type, list_names, story, 1, max_attrib)
        if object_names_adjective and len(object_names_adjective) > 0:
            print(object_names_adjective)
            for character in characters:
                if character.get_name() in object_names_adjective:
                    character.add_appearance_modifier(object_names_adjective[character.get_name()])
            if len(characters[1].get_appearance_modifiers()) > 0:
                character = characters[1]
                if character.get_name() in object_names_adjective:
                    qualities = object_names_adjective[character.get_name()]
                    if qualities:
                        print(f"{character.get_name()}: {', '.join(qualities)}")

        item_type = "actions"
        max_attrib = 1
        object_names_actions = create_object_with_call_ai(item_type, list_names, story, 1, max_attrib)
        if object_names_actions and len(object_names_actions) > 0:
            print(object_names_actions)
            for character in characters:
                if character.get_name() in object_names_actions:
                    character.add_action(object_names_actions[character.get_name()])
            if len(characters[1].get_actions()) > 0:
                character = characters[1]
                if character.get_name() in object_names_actions:
                    actions = object_names_actions[character.get_name()]
                    if actions:
                        print(f"{character.get_name()}: {', '.join(actions)}")

# OnError: repeat 3 times, if not, change promp, if not, message error
# Ask for a list of names, filter uniques, ask for more names if needed given the already generated list.
# Using list of names, ask for a list of x actions per name
# Using list of names and/or actions, ask for a list of x appearance modifiers
# Ask for a background description for all those characters, store it in a class, well organized.
# Give maximum width-tall (maxXY) and ask for XY position for each character
# Generate an image per character using each class and store it in each character class.image
# Generate a background with the background class descriptions and the maxXY
# Paste each character on top of the image using XY position.
# Optional: Create also classes of objects and buildings, generate images and paste them in background.
# Generate a new polished image with the sketched image.
# Ask an IA for validation of the image created, use info inside classes to check presence, position, quality.
# Generate percentages of compliance/efficiency, in the future use them to feedback the AIs.
# Store information in logs in order to rebuild process.
