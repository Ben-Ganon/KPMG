from flask import Flask, request
from oai import OAI_Azure

app = Flask(__name__)

oai = OAI_Azure()

@app.route('/agent', methods=['GET', 'POST'])
def agent_microservice():
    """
    This microservice is for the purpose of prompting the oai agent
    :return:
    """
    request_json = request.json
    print(f"got request: {request_json}")
    message = request_json.get("message", None)
    message = [{'role': 'user', 'metadata': {'sentiment': 'neutral'}, 'content': message}]
    history = request_json.get("history", None)
    sys_prompt = request_json.get("sys_prompt", None)
    if sys_prompt:
        history.insert(0, {'role': 'system', 'content': sys_prompt})
    print(f"sending the following conversation to the agent: {message} and history: {history}")
    if history is None or message is None:
        return None
    return oai.get_completion(message, history)

@app.route('/jsonify', methods=['POST'])
def jsonify_microservice():
    """
    This microservice is exculsively for the purpose of converting the conversation data to a json object
    :return: post reply
    """
    request_json = request.json
    print(f"got request: {request_json}")
    message = request_json.get("message", None)
    message = [{'role': 'user', 'metadata': {'sentiment': 'neutral'}, 'content': message}]
    return oai.get_completion_json(message)

def main():
    app.run(port=5000, threaded=True)

if __name__ == "__main__":
    main()