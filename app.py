import streamlit as st

st.set_page_config(page_title="同住生存指南 🏠", page_icon="🏠", layout="centered")

# 頂部視覺美化
st.markdown("<h1 style='text-align: center;'>🏠 同住批鬥法庭 & 財政部</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Just for fun，和諧共處 相親相愛喔💗</p>", unsafe_allow_html=True)
st.divider()

# 初始化 Session State
if "warnings" not in st.session_state:
    st.session_state.warnings = []

if "receipts" not in st.session_state:
    st.session_state.receipts = []

tab1, tab2 = st.tabs(["⚠️ Warning 警告信", "🧾 Debt Collection 追債"])

# ================= Tab 1: 警告信 =================
with tab1:
    st.subheader("🚨 發出罪行警告")
    with st.form("warning_form", clear_on_submit=True):
        target = st.text_input("被告人", placeholder="輸入罪人名字...")
        category = st.selectbox("罪行", [
            "🥣 食完飯無手尾", 
            "🔊 洗頭唔執頭髮", 
            "🗑️ 垃圾堆積如山", 
            "🧻 廁紙用曬唔換新",
            "❓ 其他 "
        ])
        desc = st.text_input("詳細罪狀", placeholder="救命啊...")
        
        if st.form_submit_button("🔥 發送警告信！", use_container_width=True):
            if target:
                st.session_state.warnings.insert(0, {
                    "被告": target, 
                    "罪行": category, 
                    "補充": desc or "深刻反省！",
                    "status": "pending",  # pending, denied
                    "reason": ""
                })
                st.success(f"已成功告發 {target}！")
                st.rerun()

    st.divider()
    
    # 顯示警告信列表
    if not st.session_state.warnings:
        st.info("🎉 大家要繼續相親相愛！")
    else:
        for idx, w in enumerate(st.session_state.warnings):
            with st.container(border=True):
                st.markdown(f"### ⚖️ 被告：{w['被告']}")
                st.markdown(f"**罪名：** `{w['罪行']}`")
                st.caption(f"**罪狀細節：** {w['補充']}")
                
                # 尚未處理狀態 (Pending)
                if w["status"] == "pending":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 認罪", key=f"plead_{idx}", use_container_width=True):
                            st.toast("多謝合作😘", icon="😘")
                            st.session_state.warnings.pop(idx)
                            st.rerun()
                    with col2:
                        if st.button("🙅‍♂️ 不認罪", key=f"deny_{idx}", use_container_width=True):
                            st.toast("你夠膽唔認罪😊", icon="😊")
                            st.session_state.warnings[idx]["status"] = "denied"
                            st.rerun()

                # 不認罪狀態 (Denied - 解鎖 Chat Box 辯解)
                elif w["status"] == "denied":
                    st.warning("😊 你夠膽唔認罪😊")
                    
                    if not w["reason"]:
                        # 讓被告輸入辯解理由
                        reason_input = st.text_input("💬 請交出不認罪理由：", key=f"reason_input_{idx}")
                        if st.button("提交辯解", key=f"sub_reason_{idx}"):
                            if reason_input:
                                st.session_state.warnings[idx]["reason"] = reason_input
                                st.rerun()
                    else:
                        # 顯示辯解內容與【原諒】按鈕
                        st.info(f"🗣️ **{w['被告']} 的辯解：** {w['reason']}")
                        if st.button("❤️ 原諒你啦（撤銷罪告）", key=f"forgive_{idx}", use_container_width=True):
                            st.toast("罪過已撤銷 恭喜恭喜！🕊️")
                            st.session_state.warnings.pop(idx)
                            st.rerun()

# ================= Tab 2: 追債 =================
with tab2:
    st.subheader("💸 新增追債")
    with st.form("receipt_form", clear_on_submit=True):
        title = st.text_input("Item 項目名稱", placeholder="買廁紙/今個月電費")
        
        # 📌 總金額改為純文字 Chat box 輸入，只能打字
        amount_str = st.text_input("總金額 ($)", placeholder="輸入金額")
        
        people = st.number_input("幾多人分", min_value=1, value=3, step=1)
        payer = st.text_input("代付人", placeholder="金主...")
        
        if st.form_submit_button("🧾 發起追數！", use_container_width=True):
            if title and payer and amount_str:
                # 驗證金額是否為數字
                try:
                    amount_num = float(amount_str)
                    st.session_state.receipts.insert(0, {
                        "項目": title, 
                        "總金額": amount_num, 
                        "金主": payer, 
                        "幾多人分": people, 
                        "每人磅水": round(amount_num / people, 1)
                    })
                    st.success("追數發起成功！")
                    st.rerun()
                except ValueError:
                    st.error("⚠️ 金額請只輸入數字")

    st.divider()
    
    # 顯示追債列表
    if not st.session_state.receipts:
        st.info("💵 無未結帳目，大家互不相欠！")
    else:
        for idx, r in enumerate(st.session_state.receipts):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"#### 🛍️ {r['項目']}")
                    st.caption(f"總金額：**${r['總金額']}** (由 **{r['代付人']}** 代付，{r['幾多人分']} 人平分)")
                    st.metric(label="每人應付", value=f"${r['每人應付']}")
                with col2:
                    if st.button("✅ 已找數", key=f"r_{idx}", use_container_width=True):
                        st.toast("結清帳目！👍")
                        st.session_state.receipts.pop(idx)
                        st.rerun()
