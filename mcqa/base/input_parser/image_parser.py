import base64

from mcqa.domain.input_parser import InputParser


class ImageParser(InputParser):
    """Parser class for image files to base64 encoded strings."""

    def parse(self, file_path: str):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
