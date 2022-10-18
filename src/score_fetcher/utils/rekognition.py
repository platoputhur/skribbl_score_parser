from telnetlib import Telnet
import boto3
from collections import OrderedDict
import re

class AWSRekognition:
    def __init__(self) -> None:
        self.client = boto3.client('rekognition')


    def get_text_from_image(self, image_in_base64_bytes: bytes) -> dict:
        return self.client.detect_text(Image={'Bytes': image_in_base64_bytes})

    def parse_the_names_and_points_from_detected_text(self, text_detections: dict, available_names: list) -> list:
        scores = []
        detected_text = text_detections.get("TextDetections")
        round_info_regex = re.compile(r"Round \d of \d", re.IGNORECASE)
        points_info_regex = re.compile(r"points: \d*", re.IGNORECASE)
        detected_text = [
            item for item in detected_text if not item.get("ParentId")]
        for text_details in detected_text:
            if text := text_details.get("DetectedText"):
                text = text.lower().replace("(you)", "").strip()
                if text.isdigit() or text.replace("#", "").isdigit():
                    continue
                elif round_info_regex.match(text):
                    continue
                elif points_info_regex.match(text):
                    scores.append({
                        "point": text.replace("points: ", ""),
                        "id": int(text_details.get("Id"))
                    })
                elif text in available_names:
                    scores.append({
                        "name": text,
                        "id": int(text_details.get("Id"))
                    })
        return sorted(scores, key=lambda x: x["id"])