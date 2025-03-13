# How to Run this Submission
- Clone repository
    ```bash
    git clone https://github.com/Ben-Ganon/KPMG.git
    ```
- Create conda environment
    ```bash
    conda create -n <env_name> python=3.10
    ```
- Create a .env file with the following content:
    ```env
    OAI_KEY="<Your Azure OpenAI Key>"
    OCR_KEY="<Your Azure OCR Key>"
    ```
- Activate conda environment
    ```bash
    conda activate <env_name>
    ```
- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
- To run part 1:
    ```bash
    python "Part 1/app.py"
    ```
- To Run Part 2:
  - Run the agent microservice
    ```bash
      python "Part 2/Services/agent.py"
    ```
  - Then, in a different process, run the part 2 app
    ```bash
    python "Part 2/app.py"
    ```

# Remarks and Explanations
- Part 1
  - The validation in part 1 is very basic, but it does partly work
  - Running the ocr + extraction combo can indeed improve the accuracy of parsing
  - But, because of time limits I could not implement the function that fixes the problem
  - Currently the problems are only shown to the user when the 'validate' button is pressed in the ui.
- Part 2
  - The switching mechanism is painfully basic, and essentially I am using gradio in a way it was not meant to be used.
  <br> It still works, but given more time I'd like to implement the whole UI in something more flexible that could 
    more 
    easily support multiple agents.
  - On account of lack of time, error handling and input checking is minimal, though from what I have tested gpt-4o is 
    pretty competent 
    and flexible.
  - The html files given in the part 2 files have been converted to markdown to make it more 'readable' to the 
    assistant.
  - All of the prompting exists in utils.py

# Extras I Would Have Liked to Implement Given More Time
- RAG mechanism for part 2, where instead of asking the assistant which file is the best then dumping the whole 
  content on it, I would use a rage mechanism to extract only information chunks relevant to the user's query.
- A more robust error handling mechanism in both parts
- Logging and Monitoring