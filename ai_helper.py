# ai_helper.py
import requests
import re

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'


def callAI(prompt):
    request = {
        'prompt': prompt,
        # 'max_length': 2000,
        'min_length': 10,
        'max_new_tokens': 800,
        'auto_max_new_tokens': True,
        'max_tokens_second': 0,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.6,
        'top_p': 0.4,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.15,
        'repetition_penalty_range': 0,
        'top_k': 40,
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
        'truncation_length': 1024,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        return result
    else:
        return None


def extract_list(input_text, max_items):
    # Check if "[" and "]" are present in the input text
    if "[" not in input_text or "]" not in input_text:
        return "Error: The list format is incorrect."

    # Define a regular expression pattern to find list-like structures
    pattern = r'[\[\(](.*?)[\]\)]'

    # Search for all matches of the pattern in the input text
    matches = re.findall(pattern, input_text)

    extracted_items = []

    for match in matches:
        # Split the match by commas, trim whitespace, and handle quoted elements
        elements = [element.strip().strip('"') for element in match.split(",")]
        # Filter out empty elements
        elements = [element for element in elements if element]

        extracted_items.extend(elements)

    # Remove duplicate items from the list
    unique_items = list(set(extracted_items))

    # If there are extracted items, limit the number of items to max_items
    if unique_items:
        # Remove items that are much longer than the rest
        max_length = max(len(item) for item in unique_items)
        unique_items = [item for item in unique_items if len(item) <= max_length * 2]

        # Cut the list to the specified max_items
        if len(unique_items) > max_items:
            unique_items = unique_items[:max_items]

        return unique_items

    return None


def generate_prompt(item_type, max_items, story):
    prompt = f"One answer for one instruction.\n" \
             f"Instruction: Write only a list with exactly {max_items} {item_type}. The list must have this format: " \
             f"'[{item_type}1,{item_type}2,{item_type}3,...,{item_type}{max_items}]'\n" \
             f"The {item_type} should be based on this story: {story}.\n" \
             f"Answer:"
    return prompt
