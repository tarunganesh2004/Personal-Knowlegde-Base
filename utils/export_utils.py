import json


def export_notes_to_json(db, filename):
    notes = db.get_all_notes()
    notes_data = [
        {
            "id": note["id"],
            "title": note["title"],
            "content": note["content"],
            "tags": note["tags"],
            "category": note["category"],
            "created_at": note["created_at"].isoformat(),
        }
        for note in notes
    ]
    with open(filename, "w") as f:
        json.dump(notes_data, f, indent=2)
