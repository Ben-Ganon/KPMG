import gradio as gr
from parser import Parser


def main():
    """
    simple demo using gradio to upload a pdf file and parse it into a json format
    :return:
    """
    document_parser = Parser()

    def output_json(file):
        print(f'got: {file.name}')
        result = document_parser.parse_filepath(file.name)
        return result, file.name  # Return file path to use later

    def validate(result, filepath):
        problems = document_parser.validate_json(result, filepath)
        if not problems:
            return "The JSON output is validated as correct"
        else:
            total_prob_str = "Problematic Fields During Validation:\n"
            for i, problem in problems.items():
                total_prob_str += f"Validation Attempt {i+1}:\n"
                for p in problem:
                    total_prob_str += f"{p}\n"
            return total_prob_str

    with gr.Blocks() as app:
        file_input = gr.File(label="Upload PDF")
        json_output = gr.JSON(label="JSON Output")
        validation_message = gr.Textbox(label="Validation Message", interactive=False)
        validate_button = gr.Button("Validate")

        state_filepath = gr.State()

        file_input.change(
            output_json, inputs=[file_input], outputs=[json_output, state_filepath]
        )
        validate_button.click(
            validate, inputs=[json_output, state_filepath], outputs=[validation_message]
        )

    app.launch()


if __name__ == "__main__":
    main()
