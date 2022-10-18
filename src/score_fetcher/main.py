from src.score_fetcher.utils.file_manager import read_image_file
from src.score_fetcher.utils.rekognition import AWSRekognition
import argparse

def main():
    parser = argparse.ArgumentParser(description="Detect names and scores from screenshots of scribble scoreboard")
    parser.add_argument(
        "--image", help="The screenshot of skribbl scoreboard", required=True)
    parser.add_argument(
        "--usernames", help="The comma separated list of the player usernames", required=True)
    args = parser.parse_args()
    aws_rk = AWSRekognition()
    bytes_image = read_image_file(args.image)
    available_names = [item.strip() for item in args.usernames.split(",")]
    detected_text = aws_rk.get_text_from_image(bytes_image)
    available_names = [item.lower() for item in available_names]
    parsed_scores_and_names = aws_rk.parse_the_names_and_points_from_detected_text(
        detected_text, available_names)
    print_names_and_scores(parsed_scores_and_names)


def print_names_and_scores(parsed_scores_and_names):
    name_to_point_dict = {}
    id_to_name_dict = {}
    for item in parsed_scores_and_names:
        id = item.get("id")
        if username := item.get("name"):
            name_to_point_dict[username] = 0
            id_to_name_dict[id] = username
        if point := item.get("point"):
            username_id = id - 2
            username = id_to_name_dict[username_id]
            name_to_point_dict[username] = point
    score_cards = []
    max_len = 0
    for k, v in name_to_point_dict.items():
        score_cards.append([k, v])

    len_hyphens = (28)*"-"
    print(len_hyphens)
    print('| {:15} | {:6} |'.format(*["Name", "Score"]))
    print(len_hyphens)
    for row in score_cards:
        print('| {:15} | {:6} |'.format(*row))
    print(len_hyphens)

if __name__ == "__main__":
    main()