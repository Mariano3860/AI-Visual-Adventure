import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


def run(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 400,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.75,
        'top_p': 0.2,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 1,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2024,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(result)


if __name__ == '__main__':
    story = "game of thrones"
    numCharacters = 15
    prompt = "One answer for one instruction.\n" +\
             "Instruction: Write a list with exactly " + str(numCharacters) +\
             " names. The list must have this format: " + \
             "'[name1,name2,name3,...,nameX]'\n" + \
             "The names should be based on this story: " + story + ".\n" \
             "Answer:"
    run(prompt)

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





