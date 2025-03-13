import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

endpoint = "https://eastus.api.cognitive.microsoft.com/"

key = os.getenv("OCR_KEY")

with open("OutputFormat.json", "r") as f:
    output_format = f.read().strip()

class OCR:
    """
    simple ocr class to encapsulate the desired ocr behavior
    """
    def __init__(self):
        self.document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key))

    def get_result(self, doc_path) -> AnalyzeResult:
        """
        example taken from the Microsoft Azure documentation on ocr,
        then converted to markdown for extra readability for the llm
        :param doc_path: document path
        :return:
        """
        with open(doc_path, "rb") as f:
            document_bytes = f.read()
        poller = self.document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=document_bytes),
            output_content_format=ContentFormat.MARKDOWN)
        result: AnalyzeResult = poller.result()
        return result
