from score_fetcher.utils.file_manager import read_image_file
from score_fetcher.utils.rekognition import AWSRekognition


def test_read_file():
    image_filepath = "/Users/defiant/Downloads/scribble.png"
    image = read_image_file(image_filepath)
    assert type(image) == bytes


def test_rekognize_text():
    image_filepath = "/Users/defiant/Downloads/scribble.png"
    image = read_image_file(image_filepath)
    aws_rek = AWSRekognition()
    detected_text = aws_rek.get_text_from_image(image)
    assert type(detected_text) == dict
