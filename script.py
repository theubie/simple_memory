import gradio as gr
import pickle
import modules.shared as shared
from modules.extensions import apply_extensions
from modules.text_generation import encode, get_max_prompt_length
from modules.chat import generate_chat_prompt

try:
    with open('saved_data.pkl', 'rb') as f:
        params = pickle.load(f)
except FileNotFoundError:
    params = {
        "activate": False,
        "simple memory": "*Add memories here*",
        "multiplier": 1,
    }


def custom_generate_chat_prompt(user_input, state, **kwargs):

    print(f"user_input: {user_input}\nstate: {state}\nparams: {params}")
    if params['activate']:
        state["context"] = f"{params['simple memory'].strip()}\n {state['context'].strip()} \n"

    return generate_chat_prompt(user_input, state, **kwargs)



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
