import gradio as gr
import requests
from types import SimpleNamespace
import json
from utils import phase_1_sysprompt, jsonify_prompt, phase_2_sysprompt, files_str, phase_2_query


def phase_1(message, history, state):
    """
    first phase of the conversation with a specific system prompt.
    As soon as we get the desired information we switch to phase 2 via a "<DONE>" message from the assistant indicating
    that we have all the information we need.
    :param message: user message
    :param history: conversation history
    :param state: the current app state with the phase, as well user data and history index (empty in this phase)
    :return:
    """
    print(f"sending request for message: {message} and history: {history}")
    response = requests.post("http://localhost:5000/agent", json={"message": message, "history": history,
                                                                  "sys_prompt": phase_1_sysprompt})
    if "<DONE>" in response.text:
        state.mode = "phase_2"
        full_history = history + [{'role': 'user', 'content': message}]
        history_str = ""
        for item in full_history:
            history_str += item['role'] + ": " + item['content'] + "\n"
        message = jsonify_prompt.format(history=history_str)
        output_json = requests.post("http://localhost:5000/jsonify", json={"message": message})
        output_json = json.loads(output_json.text)
        state.user_data = output_json
        state.history_index = len(full_history)
        return ("Thank you for providing your information. We will now switch to the Q&A phase. \nWhat would you like "
                "help with today?", state)
    return response.text, state


def get_relevant_file(user_query):
    """
    find the most relevant file to the user query and return the file name
    :param user_query: the user query
    :return: filename of the most relevant file (from the relevant files in the phase_2_data_md folder)
    """
    message = (f"given the following user query: {user_query}, please choose which of the following areas of "
               f"medecine is most relevant to the user: {files_str}. Answer only with one of the options as is "
               f"and nothing else")
    response = requests.post("http://localhost:5000/agent", json={"message": message, "history": []})
    return response.text


def phase_2(message, history, state):
    """
        second phase of the conversation with a specific system prompt.
        answer the user's question based on the given information in the relevant document, chosen via extra
        prompting of the assistant behind the scenes
        :param message: user message
        :param history: conversation history
        :param state: the current app state with the phase, as well user data and history index (empty in this phase)
        :return:
        """
    print(f"sending request for message: {message} and history: {history}")
    history_index = state.history_index
    user_data = state.user_data
    relevant_history = history[history_index:]
    relevant_file_name = get_relevant_file(message).strip()
    print(f"relevant file name: {relevant_file_name}")
    try:
        with open(f"Part 2/phase_2_data_md/{relevant_file_name}", "r", encoding='utf8') as f:
            file_content = f.read()
    except FileNotFoundError:
        return (f"Sorry, I couldn't find any relevant information on that! would you like to try wording it a little "
                f"diffirently?", state)
    final_query = phase_2_query.format(user_query=message, user_data=user_data, document_content=file_content)
    response = requests.post("http://localhost:5000/agent", json={"message": final_query, "history": relevant_history,
                                                                  "sys_prompt": phase_2_sysprompt})
    return response.text, state


def router(message, history, state):
    """
    switch between phases depending on state
    :param message:
    :param history:
    :param state:
    :return:
    """
    if state.mode == "phase_1":
        return phase_1(message, history, state)
    elif state.mode == "phase_2":
        return phase_2(message, history, state)


def main():
    """
    simple gradio app with a basic chat interface and a router function that switches between the two phases.
    :return:
    """
    with gr.Blocks() as app:
        state_object = SimpleNamespace(mode="phase_1", user_data={}, history_index=0)
        state = gr.State(state_object)
        print(f'state: {state}')

        chat_interface = gr.ChatInterface(
            fn=router,
            additional_inputs=[state],
            additional_outputs=[gr.State()],
            title="Medical Services Q&A",
            type="messages",
            description="Welcome to the Q&A service. You will be asked to give some information about yourself and "
                        "then the assistant will help you with your questions.",
        )

    app.launch()


if __name__ == "__main__":
    main()
