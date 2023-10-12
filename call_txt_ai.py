# call_txt_ai.py
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer


def call_txt_ai_local_AutoGPTQ(prompt):
    model_name_or_path = "TheBloke/CodeLlama-7B-Instruct-GPTQ"
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                 device_map="auto",
                                                 trust_remote_code=True,
                                                 revision="main")
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.cuda()
    output = model.generate(
        inputs=input_ids,
        do_sample=True,
        temperature=0.8,
        top_p=0.4,
        top_k=40,
        max_new_tokens=512,
        min_length=10,
        repetition_penalty=1.15,
        max_time=5000,
    )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # Manually remove the prompt from the generated text
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):].strip()
    return generated_text


def call_txt_ai_api(prompt):
    # https://huggingface.co/docs/transformers/main_classes/text_generation
    host = 'localhost:5000'
    url = f'http://{host}/api/v1/generate'
    request = {
        'prompt': prompt,
        # 'max_length': 2000,
        'min_length': 10,
        'max_new_tokens': 800,
        'auto_max_new_tokens': True,
        'max_tokens_second': 0,
        'max_time': 5000,
        'force_words_ids': [";"],
        'bad_words_ids': ["Answer", "answers", "actions", "descriptions", "adjectives", "I will", "Answer:", "answer:",
                          "http://", "\\n", "Retrieved from", "\\nAnswer:"],
        'num_return_sequences': 1,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.8,
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
    response = requests.post(url, json=request)
    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        return result
    else:
        return None
