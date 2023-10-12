from generation import create_characters

if __name__ == '__main__':
    story = "Game of thrones"
    max_items = 3
    characters = create_characters(story, max_items)
    print(characters[0].get_description())
