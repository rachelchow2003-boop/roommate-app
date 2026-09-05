import streamlit as st

st.set_page_config(page_title="同住生存指南 🏠", page_icon="🏠", layout="centered")
st.title("🏠 同住批鬥法庭 & 財政部")
st.caption("Just for fun，和諧共處相親相愛喔🤪")

# 🛠️ 初始化 Session State（改為空列表 []）
if "warnings" not in st.session_state:
    st.session_state.warnings = []

if "receipts" not in st.session_state:
    st.session_state.receipts = []

tab1, tab2 = st.tabs(["⚠️ Warning 警告信", "🧾 追債"])

# ================= Tab 1: 警告信 =================
with tab1:
    st.subheader("🚨 發出罪行警告")
    with st.form("warning_form", clear_on_submit=True):
        target = st.text_input("被告人")
        category = st.selectbox("罪行", [
            "🥣 食完飯無手尾", 
            "🔊 洗頭唔執頭髮", 
            "🗑️ 垃圾堆積如山", 
            "🧻 廁紙用曬唔換新"
        ])
        desc = st.text_input("詳細罪狀")
        if st.form_submit_button("🔥 發送警告信！", use_container_width=True):
            if target:
                st.session_state.warnings.insert(0, {
                    "被告": target, 
                    "罪行": category, 
                    "補充": desc or "深刻反省！"
                })
                st.success(f"已告發 {target}！")
                st.rerun()

    st.divider()
    
    # 顯示列表
    if not st.session_state.warnings:
        st.info("暫時天下太平，冇人被告發！🎉")
    else:
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

# ================= Tab 2: 追債 =================
with tab2:
    st.subheader("💸 新增追債")
    with st.form("receipt_form", clear_on_submit=True):
        title = st.text_input("Item")
        amount = st.number_input("總金額 ($)", min_value=1.0, value=300.0)
        people = st.number_input("幾多人分", min_value=1, value=3)
        payer = st.text_input("代付人")
        if st.form_submit_button("🧾 發起追數！", use_container_width=True):
            if title and payer:
                st.session_state.receipts.insert(0, {
                    "項目": title, 
                    "總金額": amount, 
                    "代付人": payer, 
                    "幾多人分": people, 
                    "每人應付": round(amount / people, 1)
                })
                st.success("追帳成功！")
                st.rerun()

    st.divider()
    
    # 顯示列表
    if not st.session_state.receipts:
        st.info("無未結帳目，大家互不相欠！💵")
    else:
        for idx, r in enumerate(st.session_state.receipts):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{r['項目']}** — ${r['總金額']} (由 {r['代付人']} 墊)")
                    st.metric("每人應付", f"${r['每人應付']}")
                with col2:
                    if st.button("已找數", key=f"r_{idx}"):
                        st.session_state.receipts.pop(idx)
                        st.rerun()

