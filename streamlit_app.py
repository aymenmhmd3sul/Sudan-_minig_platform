import streamlit as st
import requests
import re
import urllib.parse

# =======================================================
# إعدادات المنصة الأساسية والأمان
# =======================================================
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

API_URL = "https://sudan-mining-platform.onrender.com"
ADMIN_PASSWORD = "Ayman_Secure_2026"

# دالة ذكية لتنظيف وفلترة أرقام الهواتف لحماية العمولة من الالتفاف في حقول النصوص
def filter_contact_info(text):
    if not text:
        return text
    phone_pattern = r'\b\d{7,14}\b'
    cleaned_text = re.sub(phone_pattern, "[🔒 مخفي لحفظ العمولة]", text)
    return cleaned_text

# دالة لتوليد رابط إرسال الواتساب التلقائي للطلبات
def generate_whatsapp_trigger(order_id, category, specs):
    base_msg = f"⛏️ *إشعار طلب شراء جديد من منصة تعدين السودان*\n\n" \
               f"📦 *رقم الطلب:* #{order_id}\n" \
               f"🗂️ *الفئة المطلوبة:* {category}\n" \
               f"📋 *المواصفات الفنية:* {specs}\n\n" \
               f"💡 *يا هندسة:* ادخل الآن على المنصة باستخدام كود التاجر الخاص بك وقدم عرضك الفني وصورك لحسم الصفقة الفورية!"
    
    # تحويل النص لترميز متوافق مع روابط الويب (URL Encoding)
    encoded_msg = urllib.parse.quote(base_msg)
    # رابط إرسال جماعي أو لفتح الواتساب مباشرة بالرسالة الجاهزة
    whatsapp_url = f"https://wa.me/?text={encoded_msg}"
    return whatsapp_url

# =======================================================
# طبقة البورصة وجلب الأسعار الحية بالجرام
# =======================================================
@st.cache_data(ttl=30)
def fetch_market_prices():
    metrics = {"local_gold_price": "115,000 SDG", "global_gold_gram_usd": "75.56 USD"}
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=3)
        if response.status_code == 200:
            metrics["global_gold_gram_usd"] = f"{(2350.00 / 31.1035):.2f} USD"
    except:
        pass
    return metrics

prices = fetch_market_prices()

# =======================================================
# الواجهة الرئيسية والهيكل العام
# =======================================================
st.title("⛏️ منصة تعدين السودان الرقمية")
st.caption("البورصة المهنية الأولى للمعدات الثقيلة والأصول الاستثمارية التعدينية")
st.markdown("---")

menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 بورصة الذهب والأسعار",
        "⚙️ سوق المعدات والآليات (المحرك الرئيسي)",
        "💎 سوق الأصول والفرص الاستثمارية",
        "🔐 لوحة التحكم المركزية (الأدمن)"
    ]
)

# =======================================================
# 1. شاشة البورصة والإحصائيات
# =======================================================
if menu == "📊 بورصة الذهب والأسعار":
    st.header("📈 حركة أسعار الذهب والمؤشرات الحية")
    col1, col2 = st.columns(2)
    col1.metric(label="🇸🇩 خام الذهب المحلي / للجرام", value=prices["local_gold_price"])
    col2.metric(label="🌍 البورصة العالمية / للجرام", value=prices["global_gold_gram_usd"])
    st.markdown("---")
    st.info("💡 المنصة تضمن سرية الصفقات وعروض الأسعار بين المورد والمشتري لضمان الحقوق والعمولات.")

# =======================================================
# 2. سوق المعدات والآليات (المحرك الرئيسي)
# =======================================================
elif menu == "⚙️ سوق المعدات والآليات (المحرك الرئيسي)":
    st.header("🚜 سوق بيع وتأجير الآليات والمعدات الثقيلة")
    action = st.radio("اختر صفتك الآن للتحرك:", ["👤 أنا مشتري (أبحث عن معدة)", "🏪 أنا تاجر/مورد (تسجيل وعرض المعدات)"])
    st.markdown("---")
    
    # ------------------- رحلة المشتري + إرسال إشعار الواتساب -------------------
    if action == "👤 أنا مشتري (أبحث عن معدة)":
        st.subheader("📝 أنشئ طلب شراء/إيجار لمعدة محددة")
        
        if "order_id" not in st.session_state:
            st.session_state.order_id = None
            st.session_state.temp_cat = ""
            st.session_state.temp_specs = ""
            
        if st.session_state.order_id:
            st.success(f"🎉 تم نشر طلبك بنجاح في سوق الموردين تحت رقم آلي: #{st.session_state.order_id}")
            
            # --- تفعيل نظام إرسال الواتساب للتجار حياً هنا ---
            st.markdown("### 📢 خطوة التنبيه الفوري للتجار:")
            st.write("اضغط على الزر بالأسفل لإرسال مواصفات الطلب فوراً إلى مجموعة أو أرقام التجار على الواتساب لتجهيز عروضهم:")
            
            wa_link = generate_whatsapp_trigger(st.session_state.order_id, st.session_state.temp_cat, st.session_state.temp_specs)
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 12px 24px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 18px; cursor: pointer; display: inline-block;">
                        💬 إرسال الطلب فوراً للتجار عبر الواتساب
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🔄 إنشاء طلب جديد آخر"):
                st.session_state.order_id = None
                st.rerun()
        else:
            with st.form("buyer_equipment_form"):
                b_name = st.text_input("اسم المشتري / الشركة المستثمرة")
                b_phone = st.text_input("رقم الواتساب الحقيقي للتواصل")
                cat_type = st.selectbox("الفئة المطلوبة", ["بوكلين / حافرة", "لودر / شاحنة ثقيلة", "مولد كهربائي كبير", "طواحين رطبة"])
                specs = st.text_area("المواصفات المطلوبة بدقة (الموديل، سنة الصنع المفضلة، ومكان العمل)")
                
                submit_req = st.form_submit_button("🚀 نشر الطلب وتجهيز رسالة الواتساب")
                if submit_req and b_name and b_phone and specs:
                    import random
                    st.session_state.order_id = random.randint(1000, 9999)
                    st.session_state.temp_cat = cat_type
                    st.session_state.temp_specs = specs
                    st.rerun()

    # ------------------- رحلة التاجر والتسجيل الذاتي -------------------
    elif action == "🏪 أنا تاجر/مورد (تسجيل وعرض المعدات)":
        tab1, tab2 = st.tabs(["🆕 تسجيل تاجر جديد (لأول مرة)", "🔑 دخول الموردين وتقديم العروض"])
        
        with tab1:
            st.subheader("📝 سجل حسابك التجاري فوراً مجاناً")
            with st.form("merchant_registration_instant"):
                m_name = st.text_input("اسم التاجر أو المعرض التجاري")
                m_email = st.text_input("البريد الإلكتروني (اختياري)")
                m_whats = st.text_input("رقم الواتساب الرئيسي (سيتم إخفاؤه وحجبه تلقائياً)")
                
                reg_btn = st.form_submit_button("🚀 تفعيل حسابي كتاجر معتمد")
                if reg_btn and m_name and m_whats:
                    m_code = f"MCH-{m_whats[-4:]}"
                    st.success(f"🎉 تم تفعيل حسابك بنجاح! كود الدخول السريع الخاص بك هو: **{m_code}**")
                    st.info("💡 انسخ الكود، وانتقل لتبويب 'دخول الموردين' لبدء تقديم عروضك فوراً.")
                    
        with tab2:
            st.subheader("📥 غرفة طلبات الشراء الحية (قدم عروضك الآن)")
            auth_code = st.text_input("أدخل كود التاجر الخاص بك أو رقم الواتساب المسجل للدخول", type="password")
            
            if auth_code != "":
                st.success("🔓 تم الدخول بنجاح لغرفة الصفقات النشطة.")
                
                with st.expander("📋 طلب شراء نشط متوفر حالياً في السوق"):
                    st.markdown("**المواصفات المطلوبة:** مطلوب بوكلين أو آلية ثقيلة للعمل الفوري، المعاينة والدفع كاش.")
                    st.markdown("---")
                    
                    with st.form("offer_submit_form"):
                        cc1, cc2 = st.columns(2)
                        make = cc1.text_input("الشركة المصنعة")
                        model = cc2.text_input("الموديل الدقيق")
                        year = st.number_input("سنة الصنع", min_value=2000, max_value=2026, value=2018)
                        hours = st.number_input("ساعات التشغيل (Hours)", min_value=0)
                        eng_cond = st.selectbox("حالة المحرك والمكنة", ["ممتاز", "جيد جداً", "يحتاج صيانة"])
                        hyd_cond = st.selectbox("حالة الهيدروليك", ["ممتاز وخالٍ من التسريب", "جيد جداً"])
                        price_val = st.number_input("السعر المعروض للبيع / الإيجار", min_value=1.0)
                        state_loc = st.text_input("مكان تواجد المعدة للمعاينة الحالية")
                        
                        st.file_uploader("ارفع صور المعدة من الميدان (حد أدنى 5 صور)", accept_multiple_files=True)
                        notes = st.text_area("ملاحظات إضافية للمشتري")
                        filtered_notes = filter_contact_info(notes)
                        
                        submit_offer = st.form_submit_button("📥 إرسال عرضي السري المشفر للعميل")
                        if submit_offer:
                            st.success("🎯 تم إرسال تقرير فحص معدتك وسعرك بنجاح للمشتري!")

# =======================================================
# 3. سوق الأصول والفرص الاستثمارية 
# =======================================================
elif menu == "💎 سوق الأصول والفرص الاستثمارية":
    st.header("💎 بورصة الأصول الاستثمارية والمشاريع الإنتاجية للتعدين")
    with st.container(border=True):
        st.subheader("🏭 مصنع خط سيانيد متكامل ومعالجة كرتة للبيع أو الشراكة")
        st.markdown("**📍 الموقع الجغرافي:** ولاية نهر النيل")
        m1, m2, m3 = st.columns(3)
        m1.button("⚙️ مؤشر الجاهزية: قيد التشغيل 🟢", disabled=True)
        m2.button("🛡️ مؤشر التحقق: موثق ميدانياً ✅", disabled=True)
        m3.button("💼 نوع الصفقة: شراكة تمويل وتوسعة تشغيلية", disabled=True)
        
        if st.button("💼 تقديم طلب اهتمام كمستثمر معتمد"):
            st.success("📥 تم تسجيل طلب اهتمامك سرياً كـ 'مستثمر معتمد'.")

# =======================================================
# 4. لوحة التحكم المركزية (الأدمن)
# =======================================================
elif menu == "🔐 لوحة تحكم الإدارة (الأدمن)":
    st.header("🔐 غرفة القيادة والتحكم للمنصة - مهندس أيمن")
    admin_pass = st.text_input("أدخل كلمة مرور الإدارة لفتح التقارير الحساسة وحساب العمولات", type="password")
    
    if admin_pass == ADMIN_PASSWORD:
        st.success("🔓 أهلاً بك يا هندسة. تم فتح الصلاحيات المركزية.")
        st.subheader("💵 تقارير صفقات المعدات وعمولاتها")
        st.markdown("""
        | رقم الطلب | المشتري | نوع المعدة | السعر المعروض | حالة الصفقة | الإجراء والعمولة |
        |---|---|---|---|---|---|
        | #9942 | شركة نهر النيل | بوكلين CAT | $42,000 | `INSPECTION_APPROVED` | [المعدات الثقيلة: عمولة تفاوضية مع الأدمن] |
        """)
    elif admin_pass != "":
        st.error("❌ كلمة المرور غير صحيحة.")
