import streamlit as st
import pandas as pd
from datetime import date

# 앱 제목
st.title("🍗 단백질 추적기")

# 세션 상태 초기화
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=["날짜", "식품", "단백질량(g)"])

# 목표 단백질량 설정
daily_goal = st.sidebar.number_input("🎯 하루 목표 단백질량 (g)", value=120)

# 사용자 입력
with st.form(key="input_form"):
    food = st.text_input("식품 이름")
    protein = st.number_input("단백질량 (g)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("✅ 추가")

    if submitted and food:
        new_row = {"날짜": str(date.today()), "식품": food, "단백질량(g)": protein}
        st.session_state.log = pd.concat([st.session_state.log, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"{food} 추가 완료!")

# 오늘 날짜의 기록만 필터링
today = str(date.today())
today_log = st.session_state.log[st.session_state.log["날짜"] == today]

# 총 단백질량 계산
total = today_log["단백질량(g)"].sum()
percent = (total / daily_goal) * 100 if daily_goal > 0 else 0

# 결과 표시
st.subheader("📋 오늘의 기록")
st.dataframe(today_log, use_container_width=True)

st.metric(label="💪 총 단백질 섭취량", value=f"{total:.1f}g", delta=f"{percent:.1f}% 목표 달성")

# 파일 저장 옵션
if st.button("💾 CSV로 저장"):
    today_log.to_csv(f"protein_log_{today}.csv", index=False)
    st.success("CSV 저장 완료!")
