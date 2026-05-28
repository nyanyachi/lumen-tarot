import streamlit as st
import random

from cards import cards
from ai_reader import generate_fake_ai, generate_three_card_reading
from memory_manager import add_reading, update_feedback

if "feedback_message" not in st.session_state:
    st.session_state["feedback_message"] = None

if "today_reading" not in st.session_state:
    st.session_state["today_reading"] = None

if "three_card_reading" not in st.session_state:
    st.session_state["three_card_reading"] = None

st.sidebar.markdown("## 🔮 루멘 타로")

page = st.sidebar.radio(
    "",
    ["🏠 홈", "🌙 오늘의 타로", "🔮 3장 리딩"]
)

if page == "🏠 홈":
    st.markdown(
    """
    <h1 style='text-align: center; font-size: 48px;'>
        🔮 루멘 타로에 어서오세요
    </h1>
    <h3 style='text-align: center;'>
        오늘의 운세나 3장 리딩을 선택해보세요.
    </h3>
    """,
    unsafe_allow_html=True
)

    st.info("👈 왼쪽 사이드바에서 원하는 리딩 메뉴를 선택해보세요.")

    st.divider()

    st.subheader("🌙 메이저 아르카나 덱")

    display_items = [
    cards[0]["image"],
    "images/card_back.png",
    cards[17]["image"],
    "images/card_back.png",
    cards[18]["image"]
    ]

    cols = st.columns(5)

    for col, image_path in zip(cols, display_items):
        with col:
            st.image(image_path, use_container_width=True)

elif page == "🌙 오늘의 타로":
    st.markdown(
        """
        <h1 style='text-align: center;'>
            🌙 오늘의 타로
        </h1>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input("오늘의 고민이나 질문을 입력해보세요")

    if not question:
        st.warning("AI 해석을 위해 질문을 먼저 입력해주세요.")

    st.divider()

    if st.button("🌙 카드 뽑기", disabled=not question):
        selected_card = random.choice(cards)

        ai_result = generate_fake_ai(
            selected_card["name"],
            question
        )

        record_id = add_reading(
            question=question,
            reading_type="오늘의 타로",
            cards=[selected_card["name"]],
            ai_result=ai_result
        )

        st.session_state["today_reading"] = {
            "card": selected_card,
            "ai_result": ai_result,
            "record_id": record_id
        }


    if st.session_state["today_reading"]:
        selected_card = st.session_state["today_reading"]["card"]
        ai_result = st.session_state["today_reading"]["ai_result"]
        record_id = st.session_state["today_reading"]["record_id"]

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(selected_card["image"], width=300)

            st.markdown(
                f"""
                <h2 style='text-align: center;'>
                    {selected_card["emoji"]} {selected_card["name"]}
                </h2>
                """,
                unsafe_allow_html=True
            )

        st.info(f"✨ 키워드: {selected_card['keywords']}")

        st.markdown("### 🔮 카드의 메시지")
        st.write(selected_card["meaning"])

        st.markdown("### ✨ 루멘의 AI 해석")
        st.success(ai_result)

        col_like, col_dislike = st.columns(2)

        with col_like:
            if st.button("👍 도움이 됐어요", key="like_today"):
                update_feedback(record_id, "like")
                st.success("좋아요 피드백이 저장됐어요.")

        with col_dislike:
            if st.button("👎 별로였어요", key="dislike_today"):
                update_feedback(record_id, "dislike")
                st.warning("별로예요 피드백이 저장됐어요.")

elif page == "🔮 3장 리딩":
    st.markdown(
        """
        <h1 style='text-align: center;'>
            🔮 과거 / 현재 / 미래 리딩
        </h1>
        <h4 style='text-align: center; color: gray;'>
            세 장의 카드가 지금의 흐름을 보여줍니다
        </h4>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input("질문이나 고민을 입력해보세요")

    if not question:
        st.warning("AI 해석을 위해 질문을 먼저 입력해주세요.")

    st.divider()

    if st.button("🌙 3장 뽑기", disabled=not question):
        selected_cards = random.sample(cards, 3)
        card_names = [card["name"] for card in selected_cards]

        ai_result = generate_three_card_reading(
            card_names,
            question
        )

        record_id = add_reading(
            question=question,
            reading_type="3장 리딩",
            cards=card_names,
            ai_result=ai_result
        )

        st.session_state["three_card_reading"] = {
            "cards": selected_cards,
            "ai_result": ai_result,
            "record_id": record_id
        }

    if st.session_state["three_card_reading"]:
        selected_cards = st.session_state["three_card_reading"]["cards"]
        ai_result = st.session_state["three_card_reading"]["ai_result"]
        record_id = st.session_state["three_card_reading"]["record_id"]

        positions = ["과거", "현재", "미래"]
        cols = st.columns(3)

        for col, position, card in zip(cols, positions, selected_cards):
            with col:
                st.markdown(f"### {position}")
                st.image(card["image"], use_container_width=True)
                st.markdown(f"#### {card['emoji']} {card['name']}")
                st.info(f"✨ {card['keywords']}")
                st.write(card["meaning"])

        st.markdown("### ✨ 루멘의 AI 해석")
        st.success(ai_result)

        col_like, col_dislike = st.columns(2)

        with col_like:
            if st.button("👍 도움이 됐어요", key="like_3card"):
                update_feedback(record_id, "like")
                st.success("좋아요 피드백이 저장됐어요.")

        with col_dislike:
            if st.button("👎 별로였어요", key="dislike_3card"):
                update_feedback(record_id, "dislike")
                st.warning("별로예요 피드백이 저장됐어요.")