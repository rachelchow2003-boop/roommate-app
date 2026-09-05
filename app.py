import streamlit as st

st.set_page_config(page_title="室友生存指南 🏠", page_icon="🏠", layout="centered")
st.title("🏠 室友法庭 & 財政部")
st.caption("Casual 玩吓別認真，小心感情破裂 🤪")

if "warnings" not in st.session_state:
    st.session_state.warnings = [{"被告": "阿強", "罪行": "🧻 用的最後一張廁紙唔換新", "補充": "想害死人咩！"}]

if "receipts" not in st.session_state:
    st.session_state.receipts = [{"項目": "8月水電費", "總金額": 600, "墊付人": "Sam", "幾多人分": 3, "每人應付": 200.0}]

tab1, tab2 = st.tabs(["⚠️ 告發/警告信", "🧾 追債/追收據"])

with tab1:
    st.subheader("🚨 發出罪行警告")
    with st.form("warning_form", clear_on_submit=True):
        target = st.text_input("被告人")
        category = st.selectbox("罪行", ["🥣 𩠌汁/碗碟擺咗 3 日都唔洗", "🔊 凌晨三點開喇叭打機", "🗑️ 垃圾桶滿到積成山", "🧻 用的最後一張廁紙唔換新"])
        desc = st.text_input("詳細罪狀")
        if st.form_submit_button("🔥 發送警告信！", use_container_width=True):
            if target:
                st.session_state.warnings.insert(0, {"被告": target, "罪行": category, "補充": desc or "深刻反省！"})
                st.success(f"已告發 {target}！")
                st.rerun()

    st.divider()
    for idx, w in enumerate(st.session_state.warnings):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**被告：{w['被告']}** | {w['罪行']}")
                st.caption(f"「{w['補充']}」")
            with col2:
                if st.button("認錯", key=f"w_{idx}"):
                    st.session_state.warnings.pop(idx)
                    st.rerun()

with tab2:
    st.subheader("💸 新增追帳")
    with st.form("receipt_form", clear_on_submit=True):
        title = st.text_input("項目名稱")
        amount = st.number_input("總金額 ($)", min_value=1.0, value=300.0)
        people = st.number_input("幾多人分", min_value=1, value=3)
        payer = st.text_input("代墊人")
        if st.form_submit_button("🧾 發起追帳！", use_container_width=True):
            if title and payer:
                st.session_state.receipts.insert(0, {"項目": title, "總金額": amount, "墊付人": payer, "幾多人分": people, "每人應付": round(amount/people, 1)})
                st.success("追帳成功！")
                st.rerun()

    st.divider()
    for idx, r in enumerate(st.session_state.receipts):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{r['項目']}** — ${r['總金額']} (由 {r['墊付人']} 墊)")
                st.metric("每人應付", f"${r['每人應付']}")
            with col2:
                if st.button("已找數", key=f"r_{idx}"):
                    st.session_state.receipts.pop(idx)
                    st.rerun()
