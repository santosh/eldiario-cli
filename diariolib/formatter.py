import sys
import json

UUID_THRESHOLD = 8
DATETIME_THRESHOLD = 10
TEXT_THRESHOLD = 30

def json_to_row(json_data: dict) -> str:
    list_of_entries = json.loads(json_data)
    if list_of_entries is None:
        sys.exit("There is no diary entry to list. Start writing one.")

    template = "{entry_id} {datetime} {text}"
    # Very dirty, needs cleanup
    for entry in list_of_entries:
        print(
            template.format(
                entry_id=entry["id"][:UUID_THRESHOLD],
                datetime=entry["datetime"][:DATETIME_THRESHOLD],
                text=get_body(entry["body"], TEXT_THRESHOLD),
                )
            )


def get_body(text, threshold):
    if len(text) < threshold:
        return text.strip("\n")
    return text[:threshold] + "..."
