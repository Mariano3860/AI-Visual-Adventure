from Character import Character
from generation import create_characters, create_background
from ai_helper import call_ai, extract_list, generate_prompt_items, generate_prompt_items_with_list, \
    create_object_from_list, create_list_with_call_ai

if __name__ == '__main__':
    characters = []
    story = "juego de tronos"
    max_items = 20
    item_type = "names"
    list_names = create_list_with_call_ai(item_type, max_items, story, 1)

    if len(list_names) > 0:
        print(list_names)
        print('List length: ' + str(len(list_names)))
        characters = [Character(name) for name in list_names]
        item_type = "adjective"

        prompt2 = generate_prompt_items_with_list(item_type, list_names, story, 2)
        print("promp2: " + prompt2)
        result2 = call_ai(prompt2)
        print(result2)
        object_result = create_object_from_list(result2)
        print(object_result)

        for character in characters:
            if character.get_name() in object_result:
                character.add_appearance_modifier(object_result[character.get_name()])
        if len(characters[1].get_appearance_modifiers()) > 0:
            print(characters[1].get_name() + ' ' + characters[1].get_appearance_modifiers()[0])

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
