import random

from data.card_interpretations import CARD_INTERPRETATIONS
from data.question_patterns import QUESTION_PATTERNS
from data.common_templates import MOOD_ADVICE, CLOSING_TEMPLATES


def detect_moods(question):
    scores = {
        "love": 0,
        "career": 0,
        "anxiety": 0,
    }

    for mood, keywords in QUESTION_PATTERNS.items():
        for keyword in keywords:
            if keyword in question:
                scores[mood] += 1

    detected_moods = []

    for mood, score in scores.items():
        if score > 0:
            detected_moods.append(mood)

    if not detected_moods:
        return ["general"]

    return detected_moods


def get_card_message(card_name, moods):
    card_data = CARD_INTERPRETATIONS.get(card_name)

    if card_data is None:
        return "이 카드는 아직 해석 데이터가 준비되지 않았지만, 지금의 질문을 천천히 바라보라는 메시지를 전하고 있어요."

    selected_messages = []

    for mood in moods:
        messages = card_data.get(mood)

        if not messages:
            messages = card_data.get("general", [])

        if messages:
            selected_messages.append(random.choice(messages))

    if not selected_messages:
        return "지금은 카드의 상징을 천천히 바라보며 마음을 정리해보면 좋겠어요."

    return "\n\n".join(selected_messages)


def get_mood_advice(moods):
    mood_results = []

    for mood in moods:
        if mood in MOOD_ADVICE:
            mood_results.append(random.choice(MOOD_ADVICE[mood]))

    return "\n\n".join(mood_results)


def generate_fake_ai(card_name, question):
    moods = detect_moods(question)

    card_message = get_card_message(card_name, moods)
    mood_advice = get_mood_advice(moods)
    closing = random.choice(CLOSING_TEMPLATES)

    result = f"""
{card_message}

{mood_advice}

{closing}
""".strip()

    return result


def generate_three_card_reading(card_names, question):
    moods = detect_moods(question)

    positions = ["과거", "현재", "미래"]

    mood_advice = get_mood_advice(moods)
    closing = random.choice(CLOSING_TEMPLATES)

    result_lines = [
        "### 루멘의 3장 AI 리딩",
        "",
    ]

    for position, card_name in zip(positions, card_names):
        card_message = get_card_message(card_name, moods)

        result_lines.append(f"**[{position}] {card_name}**")
        result_lines.append(card_message)
        result_lines.append("")

    result_lines.append("### 종합 조언")
    result_lines.append(mood_advice)
    result_lines.append("")
    result_lines.append(closing)

    return "\n".join(result_lines)