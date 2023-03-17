import gradio as gr
import pickle

try:
    with open('saved_data.pkl', 'rb') as f:
        params = pickle.load(f)
except FileNotFoundError:
    params = {
	    "activate": False,
        "simple memory": "*Add memories here*",
        "multiplier": 1,
	}
	
def custom_generate_chat_prompt(user_input, max_new_tokens, name1, name2, context, chat_prompt_size, impersonate=False):
    user_input = clean_chat_message(user_input)

    if params['activate']:
        rows = [f"{params['simple memory'].strip()}\n{context.strip()}\n"]
    else:
        rows = [f"{context.strip()}\n"]

    if shared.soft_prompt:
        chat_prompt_size -= shared.soft_prompt_tensor.shape[1]
    max_length = min(get_max_prompt_length(max_new_tokens), chat_prompt_size)

    i = len(shared.history['internal']) - 1
    while i >= 0 and len(encode(''.join(rows), max_new_tokens)[0]) < max_length:
        rows.insert(1, f"{name2}: {shared.history['internal'][i][1].strip()}\n")
        if not (shared.history['internal'][i][0] == '<|BEGIN-VISIBLE-CHAT|>'):
            rows.insert(1, f"{name1}: {shared.history['internal'][i][0].strip()}\n")
        i -= 1

    if not impersonate:
        rows.append(f"{name1}: {user_input}\n")
        rows.append(apply_extensions(f"{name2}:", "bot_prefix"))
        limit = 3
    else:
        rows.append(f"{name1}:")
        limit = 2

    while len(rows) > limit and len(encode(''.join(rows), max_new_tokens)[0]) >= max_length:
        rows.pop(1)

    prompt = ''.join(rows)
    return prompt

def input_modifier(string):
    if not any((shared.args.chat, shared.args.cai_chat)):
        string = f"{params['simple memory'].strip()}\n{string}"
    return string

def ui():
    # Gradio elements
    activate = gr.Checkbox(value=params['activate'], label='Activate Memory')
    string = gr.Textbox(value=params["simple memory"], label='Memory')

    # Event functions to update the parameters in the backend
    def update_string(x):
        params.update({"simple memory": x})
        with open('saved_data.pkl', 'wb') as f:
            pickle.dump(params, f)

    def update_activate(x):
        params.update({"activate": x})
        with open('saved_data.pkl', 'wb') as f:
            pickle.dump(params, f)

    string.change(update_string, string, None)
    activate.change(update_activate, activate, None)
