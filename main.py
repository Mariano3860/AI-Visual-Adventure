from generation import create_characters, create_background
from ai_helper import callAI, extract_list, generate_prompt

if __name__ == '__main__':
    story = "juego de tronos"
    max_items = 20
    item_type = "names"
    prompt = generate_prompt(item_type, max_items, story)
    result = callAI(prompt)

    if result:
        print("result: " + result)
        extracted_result = extract_list(result, max_items)
        if extracted_result and len(extracted_result) > 0:
            print(extracted_result)
            print('List length: ' + str(len(extracted_result)))
        else:
            print("Error extracting list: " + result)
            print(extracted_result)
    else:
        print("AI request failed.")

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
