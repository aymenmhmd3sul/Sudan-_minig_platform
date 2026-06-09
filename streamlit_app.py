import streamlit as st

st.set_page_config(page_title="منصة تعدين السودان الرقمية", layout="wide")

# ===== SIDEBAR =====
st.sidebar.title("📌 القائمة")

page = st.sidebar.radio(
    "التنقل",
    ["📊 الداشبورد", "🛒 المشتري", "🏪 التاجر", "🤝 الصفقات", "⚙️ النظام"]
)

# ===== DASHBOARD =====
if page == "📊 الداشبورد":
    st.title("📊 الداشبورد")
    st.success("النظام يعمل بشكل طبيعي")

# ===== BUYER =====
elif page == "🛒 المشتري":
    st.title("🛒 المشتري")
    st.selectbox("نوع المعدات", ["معدات خفيفة", "معدات ثقيلة"])

# ===== SELLER =====
elif page == "🏪 التاجر":
    st.title("🏪 التاجر")

# ===== DEALS =====
elif page == "🤝 الصفقات":
    st.title("🤝 الصفقات")

# ===== SYSTEM =====
elif page == "⚙️ النظام":
    st.title("⚙️ معلومات النظام")
    st.info("النظام يعمل بشكل مستقر")
