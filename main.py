from Character import Character
from text_ai_helper import create_list_with_call_ai, create_object_with_call_ai

if __name__ == '__main__':
    characters = []
    story = "Harry potter"
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

