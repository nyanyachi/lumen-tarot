import streamlit as st
import random
from cards import cards
from ai_reader import generate_fake_ai
from ai_reader import generate_three_card_reading



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

        col1, col2, col3 = st.columns([1,2,1])

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

        if question:

            ai_result = generate_fake_ai(
                selected_card["name"],
                question
            )       

        st.markdown("### ✨ 루멘의 AI 해석")

        st.success(ai_result)

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

    if st.button("🔮 3장 뽑기", disabled=not question):
        selected_cards = random.sample(cards, 3)

        positions = ["과거", "현재", "미래"]

       

        cols = st.columns(3)

        for col, position, card in zip(cols, positions, selected_cards):
            with col:
                st.markdown(
                    f"""
                    <h2 style='text-align: center;'>
                        {position}
                    </h2>
                    """,
                    unsafe_allow_html=True
                )

                st.image(card["image"], use_container_width=True)

                st.markdown(
                    f"""
                    <h3 style='text-align: center;'>
                        {card["emoji"]} {card["name"]}
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

                st.info(f"✨ {card['keywords']}")

                st.write(card["meaning"])

        if question:
                st.success(f"'{question}'에 대한 과거/현재/미래 리딩입니다.")

                reading = generate_three_card_reading(
                    [card["name"] for card in selected_cards],
                    question
                )

                st.divider()

                st.subheader("🔮 루멘의 AI 해석")
                st.markdown(reading)