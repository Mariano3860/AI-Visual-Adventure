# Implementation

## Implementation steps

1. Ask for a list of names, filter uniques, ask for more names if needed given the already generated list.
   - OnError: repeat 3 times, if not, change prompt, if not, message error
2. Using list of names, ask for a list of x actions per name
   - OnError: repeat 3 times, if not, change prompt, if not, message error
3. Using list of names and/or actions, ask for a list of x appearance modifiers
   - OnError: repeat 3 times, if not, change prompt, if not, message error
4. Ask for a background description for all those characters, store it in a class, well organized.
   - OnError: repeat 3 times, if not, change prompt, if not, message error
5. Give maximum width-tall (maxXY) and create XY position for each character
   - Create a map(x,y) with maxXY, and randomize position of character
       - Mark on map occupied surface of each character, randomize over free spaces.
       - Position of each character can start in top left corner and consider surface with width and length.
6. Generate an image per character using each class and store it in each character class.image
   - Generate a string Character.getDescription() method
   - Generate the image, create a right prompt and right parameters needed
     - Try to generate it from textToImg
         - If not possible, use imgToImg and use 5-10 templates depending on action
     - Use or create a test to check if character has face, full-body, if not, repeat process.
       - Use a model imgToTxt? Search for solution with less resources
     - Erase background
       - https://www.geeksforgeeks.org/how-to-remove-the-background-from-an-image-using-python/
7. Generate a background with the background class descriptions and the maxXY
     - Validate background somehow, if not repeat process
8. Paste each character on top of the image using XY position.
9. Optional: Create also classes of objects and buildings, generate images and paste them in background.
10. Generate a new polished image with the sketched image.
     - Can ask in that generation for interaction between objects.
     - Ask an IA for validation of the image created, use info inside classes to check presence, position, quality.
     - If validation is not passed, then regenerate image.
     - Generate percentages of compliance/efficiency, in the future use them to feedback the AIs.
11. Store information in logs in order to rebuild process.
     - Store all the used seeds, in text and image.