import base64


def read_image_file(image_filepath):
    image = None
    with open(image_filepath, "rb") as image_file_data:
        image_b64 = base64.b64encode(image_file_data.read())
        image = base64.decodebytes(image_b64)
    return image
