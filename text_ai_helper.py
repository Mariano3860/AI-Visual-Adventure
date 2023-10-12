# text_ai_helper.py
from call_txt_ai import call_txt_ai_local_AutoGPTQ


def generate_prompt_items(item_type, max_items, story, num_type):
    if num_type == 1:
        prompt = f"One answer for one instruction.\n" \
                 f"Instruction: Write only a list with exactly {max_items} {item_type}. The list must have this format: " \
                 f"{item_type}1;{item_type}2;{item_type}3;...;{item_type}{max_items}\n" \
                 f"The {item_type} should be based on this story: {story}.\n" \
                 f"Answer:"
    elif num_type == 2:
        prompt = f"One answer for one instruction.\n" \
                 f"Instruction: Construct a list that consists of precisely {max_items} {item_type}. The required format for the list is: " \
                 f"{item_type}1;{item_type}2;{item_type}3;...;{item_type}{max_items}\n" \
                 f"The {item_type} you include should be influenced by the narrative of {story}.\n" \
                 f"Answer:"
    else:
        prompt = f"One answer for one instruction.\n" \
                 f"Instruction: Compose a list comprising {max_items} {item_type} exactly. The list format must adhere to this pattern: " \
                 f"{item_type}1; {item_type}2; {item_type}3; ...;{item_type}{max_items}\n" \
                 f"The {item_type} you include should be related to the story of {story}.\n" \
                 f"Answer:"
    return prompt


def generate_prompt_items_with_list(item_type, item_list, story, max_attributes, num_type):
    if num_type == 1:
        prompt = f"One answer for one instruction.\n" \
                 f"Use this original list as a reference: {item_list}\n" \
                 f"Instruction: Create a list containing {max_attributes} {item_type} for each item in the list, related to the story: '{story}'. " \
                 f"Use only this format to answer: " \
                 f"'{item_list[0]}:{item_type}1,...,{item_type}{max_attributes};{item_list[1]}:{item_type}1,...,{item_type}{max_attributes};...;{item_list[len(item_list) - 1]}:{item_type}1,...,{item_type}{max_attributes}'\n" \
                 f"Answer:"
    elif num_type == 2:
        prompt = f"One answer for one instruction.\n" \
                 f"Use this original list as a reference: {item_list}\n" \
                 f"Instruction: Create a list containing one or two {item_type} for each item in the list, related to the story: '{story}'. " \
                 f"Use only this format to answer: " \
                 f"'{item_list[0]}:{item_type}1,{item_type}2;{item_list[1]}:{item_type}1,{item_type}2;...;{item_list[len(item_list) - 1]}:{item_type}1,{item_type}2'\n" \
                 f"Answer:"
    else:
        prompt = f"One answer for one instruction.\n" \
                 f"Use this original list as a reference: {item_list}\n" \
                 f"Instruction: Create a list containing one {item_type} for each item in the list, related to the story: '{story}'. " \
                 f"Use only this format to answer: " \
                 f"'{item_list[0]}:{item_type};{item_list[1]}:{item_type};...;{item_list[len(item_list) - 1]}:{item_type}'\n" \
                 f"Answer:"
    return prompt


def extract_list(input_text, max_items):
    input_text = input_text.strip("[").strip("]").strip("\'").strip("\"").strip("{").strip("}").replace("  ", " ") \
        .replace(" ;", ";").replace("; ", ";").strip(":").strip("\\n").strip().replace("Answer: ",";").replace("Answer:",";")
    extracted_list = input_text.split(';')
    if not extracted_list or len(extracted_list) <= 1:
        print("Incorrect format of input object validate_and_parse_list(): " + input_text)
        return None
    # Limit the number of items in the list based on max_items
    if max_items is not None:
        extracted_list = extracted_list[:max_items]
    # Remove items with more than 4 words
    extracted_list = [item for item in extracted_list if len(item.split()) <= 4]
    # Extract unique ones
    unique_list = list(set(extracted_list))
    return unique_list


def extract_object_from_list(input_list, max_attributes):
    try:
        input_list = input_list.strip("[").strip("]").strip("\'").strip("\"").strip("{").strip("}").replace("  ", " ") \
            .replace(" ;", ";").replace("; ", ";").strip(".").strip()
        pairs = input_list.split(';')
        if not pairs or len(pairs) < 1:
            raise ValueError("Incorrect format of input object validate_and_parse_list(): " + input_list)
        pairs = pairs[:len(input_list)]
        extracted_object = {}
        for pair in pairs:
            # Split each pair by a colon to separate name and attributes
            name, attributes_str = pair.split(':')
            # Split the attributes by commas and create a list
            attributes = attributes_str.split(',')
            # Check if max_attributes is specified and limit the number of attributes
            if max_attributes is not None:
                attributes = attributes[:max_attributes]
            # Remove attributes with more than 3 words
            attributes = [attr for attr in attributes if len(attr.split()) <= 4]
            # Add the name and attributes to the result dictionary
            extracted_object[name] = attributes
        return extracted_object
    except ValueError as e:
        print(str(e) + input_list)
        return None


def create_list_with_call_ai(item_type, max_items, story, prompt_type, retries=3):
    if retries <= 0:
        print("Error creating list with create_list_with_call_ai()\n")
        return None
    prompt = generate_prompt_items(item_type, max_items, story, prompt_type)
    result = call_txt_ai_local_AutoGPTQ(prompt)
    if result:
        extracted_result = extract_list(result, max_items)
        if extracted_result and max_items * 0.8 < len(extracted_result) < max_items * 1.2:
            return extracted_result
    # Retry with the next prompt type
    return create_list_with_call_ai(item_type, max_items, story, prompt_type + 1, retries - 1)


def create_object_with_call_ai(item_type, list_names, story, prompt_type, max_attributes=2, retries=3):
    if retries <= 0:
        print("Error creating object with create_object_with_call_ai()\n")
        return None
    prompt = generate_prompt_items_with_list(item_type, list_names, story, max_attributes, prompt_type)
    result = call_txt_ai_local_AutoGPTQ(prompt)
    if result:
        items_quality = extract_object_from_list(result, max_attributes)
        if items_quality and len(items_quality) > 0:
            return items_quality
    # Retry with the next prompt type
    return create_object_with_call_ai(item_type, list_names, story, prompt_type + 1, retries - 1)
