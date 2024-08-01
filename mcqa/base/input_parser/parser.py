from mcqa.base.input_parser.image_parser import ImageParser
from mcqa.base.input_parser.pdf_parser import PdfParser
from mcqa.domain.input_parser import InputParser


class Parser(InputParser):
    def __init__(self):
        self.pdf_parser = PdfParser()
        self.image_parser = ImageParser()

    def parse(self, file_path: str):
        if file_path is None:
            return None
        if file_path.endswith(".pdf"):
            return self.pdf_parser.upload_pdf(file_path=file_path)

        if file_path.endswith((".jpg", ".png", ".jpeg")):
            return self.image_parser.parse(file_path=file_path)
