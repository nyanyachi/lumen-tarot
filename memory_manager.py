import json
import uuid
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("reading_history.json")


def load_history():
    if not HISTORY_FILE.exists():
        return []

    if HISTORY_FILE.stat().st_size == 0:
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def add_reading(question, reading_type, cards, ai_result):
    history = load_history()

    record_id = str(uuid.uuid4())

    new_record = {
        "id": record_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "reading_type": reading_type,
        "cards": cards,
        "ai_result": ai_result,
        "feedback": None
    }

    history.append(new_record)
    save_history(history)

    return record_id


def update_feedback(record_id, feedback):
    history = load_history()

    for record in history:
        if record["id"] == record_id:
            record["feedback"] = feedback
            break

    save_history(history)