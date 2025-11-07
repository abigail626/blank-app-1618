# ...existing code...
import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="주사위 굴리기 🎲", layout="centered")

st.title("🎲 주사위 굴리기 앱")

col1, col2 = st.columns(2)
with col1:
    dice_count = st.slider("굴릴 주사위 개수", min_value=1, max_value=10, value=1)
with col2:
    sides = st.selectbox("주사위 면 수", options=[4, 6, 8, 10, 12, 20], index=1)

if "history" not in st.session_state:
    st.session_state.history = []  # 각 항목: dict(timestamp, count, sides, rolls, total)

def do_roll():
    rolls = [random.randint(1, sides) for _ in range(dice_count)]
    total = sum(rolls)
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "count": dice_count,
        "sides": sides,
        "rolls": rolls,
        "total": total,
    }
    st.session_state.history.insert(0, entry)  # 최신을 맨 위에

st.button("굴리기", on_click=do_roll)

if st.session_state.history:
    latest = st.session_state.history[0]
    st.subheader("최근 결과")
    st.write(f"시간: {latest['timestamp']}")
    st.write(f"주사위: {latest['count']}개, 면수: {latest['sides']}")
    st.write("개별 결과:", latest["rolls"])
    st.write("합계:", latest["total"])
    st.write("평균:", round(sum(latest["rolls"]) / len(latest["rolls"]), 2))

    # 히스토그램(값별 빈도)
    counts = pd.Series(latest["rolls"]).value_counts().sort_index()
    st.bar_chart(counts)

st.markdown("---")
st.subheader("굴린 기록")
if st.session_state.history:
    # 테이블로 보기
    table = []
    for e in st.session_state.history:
        table.append({
            "시간": e["timestamp"],
            "개수": e["count"],
            "면수": e["sides"],
            "합계": e["total"],
            "개별": ", ".join(map(str, e["rolls"])),
        })
    df = pd.DataFrame(table)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("기록 다운로드 (CSV)", data=csv, file_name="dice_history.csv", mime="text/csv")

    if st.button("기록 초기화"):
        st.session_state.history.clear()
        st.experimental_rerun()
else:
    st.write("아직 굴린 기록이 없습니다. '굴리기'를 눌러 시작하세요.")
# ...existing code...
