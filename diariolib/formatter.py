import json

def json_to_row(json_data: dict) -> str:
    list_of_entries = json.loads(json_data)
    template = "{entry_id} {datetime} {text}"
    for entry in list_of_entries:
        print(template.format(entry_id=entry["id"],
                              datetime=entry["datetime"],
                              text=entry["body"]))
