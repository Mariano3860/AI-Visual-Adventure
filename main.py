from Character import Character
from ai_helper import create_list_with_call_ai, create_object_with_call_ai

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

#   Ask for a list of names, filter uniques, ask for more names if needed given the already generated list.
#       OnError: repeat 3 times, if not, change prompt, if not, message error
#   Using list of names, ask for a list of x actions per name
#       OnError: repeat 3 times, if not, change prompt, if not, message error
#   Using list of names and/or actions, ask for a list of x appearance modifiers
#       OnError: repeat 3 times, if not, change prompt, if not, message error
#   Ask for a background description for all those characters, store it in a class, well organized.
#       OnError: repeat 3 times, if not, change prompt, if not, message error
#   Give maximum width-tall (maxXY) and create XY position for each character
#       Create a map(x,y) with maxXY, and randomize position of character
#           Mark on map occupied surface of each character, randomize over free spaces.
#           Position of each character can start in top left corner and consider surface with width and length.
#   Generate an image per character using each class and store it in each character class.image
#       Generate a string Character.getDescription() method
#       Generate the image, create a right prompt and right parameters needed
#       Use or create a test to check if character has face, full-body, if not, repeat process.
#   Generate a background with the background class descriptions and the maxXY
#       Validate background somehow, if not repeat process
#   Paste each character on top of the image using XY position.
#   Optional: Create also classes of objects and buildings, generate images and paste them in background.
#   Generate a new polished image with the sketched image.
#       Can ask in that generation for interaction between objects.
#       Ask an IA for validation of the image created, use info inside classes to check presence, position, quality.
#       If validation is not passed, then regenerate image.
#       Generate percentages of compliance/efficiency, in the future use them to feedback the AIs.
#   Store information in logs in order to rebuild process.
#       Store all the used seeds, in text and image.
