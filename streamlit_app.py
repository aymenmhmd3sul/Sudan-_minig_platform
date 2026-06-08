import streamlit as st
import requests
import re
import urllib.parse
import random

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="منصة تعدين السودان الرقمية",
    page_icon="⛏️",
    layout="wide"
)

# =========================
# 🎨 تصميم بصري احترافي
# =========================
st.markdown("""
<style>
.main {
    background-color: #0B0F14;
    color: white;
}

h1, h2, h3 {
    color: #D4AF37 !important;
}

.stMetric {
    background-color: #111827;
    border: 1px solid #D4AF37;
    padding: 12px;
    border-radius: 12px;
}

.stButton > button {
    background-color: #D4AF37;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}
</style>
""", unsafe_allow_html=True)

# =========================
# إعدادات النظام
# =========================
API_URL = "https://sudan-mining-platform.onrender.com"
ADMIN_PASSWORD = "Ayman_Secure_2026"

# =========================
# أدوات مساعدة
# =========================
def filter_contact_info(text):
    if not text:
        return text
    return re.sub(r'\b\d{7,14}\b', "[محجوب]", text)

def generate_whatsapp_trigger(order_id, category, specs):
    msg = f"""⛏️ طلب جديد #{order_id}
الفئة: {category}
المواصفات: {specs}"""
    return "https://wa.me/?text=" + urllib.parse.quote(msg)

@st.cache_data(ttl=30)
def fetch_market_prices():
    return {
        "local": "115,000 SDG",
        "global": "75.56 USD"
    }

prices = fetch_market_prices()

# =========================
# HEADER
# =========================
st.title("⛏️ منصة تعدين السودان الرقمية")
st.caption("بورصة الذهب والمعدات والفرص الاستثمارية")
st.markdown("---")

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 القائمة",
    [
        "📊 السوق المالي",
        "🚜 المعدات الثقيلة",
        "💎 الفرص الاستثمارية",
        "🔐 الإدارة"
    ]
)

# =========================
# 1) السوق المالي
# =========================
if menu == "📊 السوق المالي":

    st.subheader("📈 أسعار الذهب الحية")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🇸🇩 المحلي", prices["local"])
    c2.metric("🌍 العالمي", prices["global"])
    c3.metric("📊 الاتجاه", "صاعد 🔥")
    c4.metric("⚡ التحديث", "30s")

    st.markdown("---")
    st.info("نظام سوق ذهبي مباشر لعرض الأسعار والتحركات في الوقت الحقيقي.")

# =========================
# 2) المعدات الثقيلة
# =========================
elif menu == "🚜 المعدات الثقيلة":

    st.subheader("🚜 سوق المعدات والآليات")

    action = st.radio("الدور:", ["مشتري", "تاجر"])

    st.markdown("---")

    # ---------- المشتري ----------
    if action == "مشتري":

        if "order_id" not in st.session_state:
            st.session_state.order_id = None

        if st.session_state.order_id:
            st.success(f"تم إنشاء طلب #{st.session_state.order_id}")

            link = generate_whatsapp_trigger(
                st.session_state.order_id,
                st.session_state.cat,
                st.session_state.specs
            )

            st.markdown(f"""
            <a href="{link}" target="_blank">
            <button style="background:#25D366;color:white;padding:12px;border-radius:8px;">
            إرسال الطلب للتجار
            </button>
            </a>
            """, unsafe_allow_html=True)

            if st.button("طلب جديد"):
                st.session_state.order_id = None
                st.rerun()

        else:
            with st.form("buyer"):
                name = st.text_input("الاسم")
                phone = st.text_input("الواتساب")
                cat = st.selectbox("الفئة", ["بوكلين", "لودر", "مولد", "طواحين"])
                specs = st.text_area("المواصفات")

                if st.form_submit_button("نشر الطلب") and name and phone:
                    st.session_state.order_id = random.randint(1000, 9999)
                    st.session_state.cat = cat
                    st.session_state.specs = specs
                    st.rerun()

    # ---------- التاجر ----------
    else:

        st.subheader("غرفة العروض")

        code = st.text_input("كود الدخول")

        if code:
            st.success("تم الدخول")

            with st.form("offer"):
                c1, c2 = st.columns(2)

                make = c1.text_input("الشركة")
                model = c2.text_input("الموديل")

                year = st.number_input("السنة", 2000, 2026, 2018)
                price = st.number_input("السعر")

                notes = st.text_area("ملاحظات")

                if st.form_submit_button("إرسال العرض"):
                    st.success("تم إرسال العرض للمشتري")

# =========================
# 3) الفرص الاستثمارية
# =========================
elif menu == "💎 الفرص الاستثمارية":

    st.subheader("💎 مشاريع استثمارية")

    st.markdown("""
    ### 🏭 مصنع تعدين جاهز
    - موقع: نهر النيل  
    - حالة: جاهز للتشغيل  
    - نوع: شراكة
    """)

    if st.button("طلب اهتمام"):
        st.success("تم تسجيل اهتمامك")

# =========================
# 4) الإدارة
# =========================
elif menu == "🔐 الإدارة":

    st.subheader("لوحة التحكم")

    pw = st.text_input("كلمة المرور", type="password")

    if pw == ADMIN_PASSWORD:
        st.success("تم الدخول")

        st.table({
            "طلب": ["#1001"],
            "حالة": ["نشط"],
            "عمولة": ["قيد الحساب"]
        })

    elif pw:
        st.error("خطأ في كلمة المرور")
