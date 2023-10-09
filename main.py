from generation import create_characters

if __name__ == '__main__':
    story = "Harry potter"
    max_items = 10
    characters = create_characters(story, max_items)
    print(characters[0].get_description())
