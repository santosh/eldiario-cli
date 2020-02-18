import sys
import json

def json_to_row(json_data: dict) -> str:
    list_of_entries = json.loads(json_data)
    if list_of_entries is None:
        sys.exit("There is no diary entry to list. Start writing one.")
    template = "{entry_id} {datetime} {text}"
    for entry in list_of_entries:
        print(template.format(entry_id=entry["id"],
                              datetime=entry["datetime"],
                              text=entry["body"]))
