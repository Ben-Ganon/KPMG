from ocr import OCR
from oai import OAI_Azure


class Parser:
    """
    The Parser class is responsible for streamlining the process of parsing a file, prompting an assistant to extract
    relevant fields, then validating the output JSON.
    """
    def __init__(self):
        self.ocr = OCR()
        self.oai = OAI_Azure()
        with open("OutputFormat.json", "r") as f:
            output_format = f.read().strip()
        self.output_format = output_format
        self.validation_attempts = 3

    def get_validation_problems(self, original, validation):
        """
        attempt to find the causes of a failed validation and return a list of problems
        :param original:
        :param validation:
        :return:
        """
        problems = []
        for key in original:
            if key not in validation:
                problems.append(f"Key {key} is missing from the validation")
            if original[key] != validation[key]:
                problems.append(f"Key {key} has a different value in the validation")
        return problems

    def validate_json(self, json_data, filepath):
        """
        validate the json data against the output received from the OCR
        :param json_data:
        :param filepath:
        :return:
        """
        all_problems = {}
        for i in range(self.validation_attempts):
            result = self.parse_filepath(filepath)
            if result != json_data:
                problems = self.get_validation_problems(json_data, result)
                all_problems[i] = problems
                break
        return all_problems

    def parse_filepath(self, filepath) -> (dict, str):
        """
        parse the file and return the JSON output
        :param filepath:
        :return:
        """
        ocr_result = self.ocr.get_result(filepath)

        oai_query = f"""
        The following is the expected JSON output format:
        {self.output_format}

        The following is the parsed output from the OCR result:
        {ocr_result.content}
        please extract all information into the relevant fields and output the JSON format.
        """

        result = self.oai.get_completion_json_output(oai_query)
        return result
