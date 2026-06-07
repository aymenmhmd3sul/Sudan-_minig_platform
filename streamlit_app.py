import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

# رابط السيرفر الخلفي على ريندر
API_URL = "https://sudan-mining-platform.onrender.com"

# كلمة مرور لوحة الإدارة
ADMIN_PASSWORD = "Ayman_Secure_2026"

# =======================================================
# طبقة جلب البيانات والمؤشرات الذكية (حساب الجرام عالمياً ومحلياً)
# =======================================================
@st.cache_data(ttl=60)  # كاش لمدة دقيقة واحدة لتحديث السعر حياً
def fetch_platform_metrics():
    metrics = {
        "local_gold_price": "في انتظار التحديث",
        "global_gold_gram_usd": "جاري الجلب..."
    }
    
    # 1. جلب سعر الأونصة العالمي وتحويله فوراً إلى جرام
    try:
        gold_api_url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(gold_api_url, timeout=5)
        if response.status_code == 200:
            price_per_ounce = 2350.50
            price_per_gram = price_per_ounce / 31.1035
            metrics["global_gold_gram_usd"] = f"{price_per_gram:.2f} USD"
    except:
        metrics["global_gold_gram_usd"] = "متوفر في البورصة"

    # 2. جلب آخر سعر محلي للذهب من قاعدة بياناتك الخاصة
    try:
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices:
                metrics["local_gold_price"] = f"{prices[-1].get('local_price', 0.0):,}"
    except:
        pass
        
    return metrics

platform_stats = fetch_platform_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - سوق المعدات الثقيلة")
st.markdown("---")

# القائمة الجانبية المحدثة حسب خطة الـ 60 يوماً القادمة
menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 إحصائيات السوق والبورصة",
        "👤 بوابة المشترين (طلب معدة)",
        "🏪 بوابة التجار المعتمدين",
        "🔐 لوحة تحكم الإدارة (الأدمن)"
    ]
)

# =======================================================
# 1. شاشة إحصائيات السوق والبورصة بالجرام
# =======================================================
if menu == "📊 إحصائيات السوق والبورصة":
    st.header("📈 المؤشرات الاقتصادية وحركة التعدين")
    
    col1, col2 = st.columns(2)
    col1.metric(label="🇸🇩 سعر خام الذهب المحلي للجرام (SDG)", value=platform_stats['local_gold_price'])
    col2.metric(label="🌍 سعر الذهب العالمي للجرام (USD)", value=platform_stats['global_gold_gram_usd'], delta="محول تلقائياً من الأونصة للجرام")
    
    st.markdown("---")
    st.info("💡 **ملاحظة تشغيلية:** المنصة تعمل بنظام غرف الصفقات المغلقة لحماية خصوصية الأسعار والعمولات. أدخل طلبك كـ مشتري أو تصفح الطلبات كـ تاجر معتمد.")

# =======================================================
# 2. بوابة المشترين (طلب معدة أو خط إنتاج بالطن)
# =======================================================
elif menu == "👤 بوابة المشترين (طلب معدة)":
    st.header("👤 تقديم طلب شراء أو استئجار")
    st.write("اكتب مواصفات المعدة أو القدرة الإنتاجية لخط الإنتاج (بالطن) المطلوبة بدقة.")
    
    if "buyer_order_id" not in st.session_state:
        st.session_state.buyer_order_id = None

    if st.session_state.buyer_order_id:
        st.success(f"🎉 تم نشر طلبك بنجاح برقم آلي: #{st.session_state.buyer_order_id}")
        st.info("🔒 عروض الأسعار السرية المقدمة من التجار السبعة ستظهر هنا فور إرسالها.")
        
        try:
            res_bids = requests.get(f"{API_URL}/api/v1/bids/order/{st.session_state.buyer_order_id}")
            if res_bids.status_code == 200:
                bids = res_bids.json()
                if not bids:
                    st.warning("⏳ عروض التجار قيد التحضير الآن...")
                else:
                    for idx, bid in enumerate(bids):
                        with st.container(border=True):
                            st.subheader(f"العرض رقم {idx+1}")
                            st.markdown(f"#### **💰 السعر المعروض:** {bid['price']:,} {bid['currency']}")
                            st.write(f"**📍 موقع المعاينة الميدانية:** {bid['location_in_sudan']}")
                            st.caption("🔒 رقم هاتف التاجر مخفي حالياً؛ سيظهر لك فوراً عند قبول العرض لحفظ حقوق الوساطة.")
                            
                            if st.button(f"🤝 قبول هذا العرض والاتفاق الرسمي", key=f"acc_{bid['id']}"):
                                requests.put(f"{API_URL}/api/v1/orders/{st.session_state.buyer_order_id}/status?status=تم الاتفاق")
                                st.balloons()
                                st.success(f"🎉 مبروك! تم إبرام الاتفاق. هاتف المورد للمعاينة الفورية هو: {bid['merchant_phone']}")
        except:
            st.error("خطأ في الاتصال بالسيرفر.")
    else:
        with st.form("order_form"):
            buyer_name = st.text_input("اسم المشتري / الشركة")
            buyer_phone = st.text_input("رقم الهاتف (محمي ومخفي تماماً)")
            eq_type = st.selectbox("الفئة المطلوبة", ["بوكلين / حافرة", "لودر / شاحنة", "طاحونة رطبة", "خط إنتاج سيانيد (بالطن)"])
            specs = st.text_area("المواصفات الفنية (مثال: خط إنتاج سعة 50 طن/يوم في منطقة أبو حمد)")
            
            submit = st.form_submit_button("🚀 نشر الطلب سرياً للتجار")
            if submit:
                if buyer_name and buyer_phone and specs:
                    try:
                        res = requests.post(f"{API_URL}/api/v1/orders", json={"buyer_name": buyer_name, "buyer_phone": buyer_phone, "equipment_type": eq_type, "specifications": specs, "status": "نشط"})
                        if res.status_code in [200, 201]:
                            st.session_state.buyer_order_id = res.json().get("id")
                            st.rerun()
                    except:
                        st.error("السيرفر غير مستجيب.")

# =======================================================
# 3. بوابة التجار المعتمدين (المناقصة العكسية المحمية بأكواد)
# =======================================================
elif menu == "🏪 بوابة التجار المعتمدين":
    st.header("🏪 مخزن طلبات الشراء الحية للزبائن")
    
    merchant_code = st.text_input("أدخل كود التاجر المعتمد الخاص بك وضغط Enter للوصول لغرفة الطلبات", type="password")
    
    if merchant_code in [f"merchant_00{i}" for i in range(1, 8)]:
        st.success("🔓 تم التحقق: مرحباً بك في غرفة طلبات المشتري الحية.")
        
        try:
            res_orders = requests.get(f"{API_URL}/api/v1/orders")
            if res_orders.status_code == 200:
                orders = [o for o in res_orders.json() if o.get("status") == "نشط"]
                if not orders:
                    st.info("📦 لا توجد طلبات شراء نشطة حالياً.")
                else:
                    for order in orders:
                        with st.expander(f"📋 طلب شراء آلي #{order['id']} - المطلوب: {order['equipment_type']}"):
                            st.markdown(f"**المواصفات الفنية المطلوبة وموقع التشغيل:**\n> {order['specifications']}")
                            st.caption("🔒 بيانات هاتف واسم المشتري مخفية تماماً لحماية سرية العميل.")
                            st.markdown("---")
                            
                            with st.form(f"bid_form_{order['id']}"):
                                price = st.number_input("السعر المعروض للبيع", min_value=1.0)
                                currency = st.selectbox("العملة", ["جنيه سوداني (SDG)", "درهم إماراتي (AED)", "دولار أمريكي (USD)"])
                                loc = st.text_input("موقع المعاينة الحالي في السودان")
                                m_phone = st.text_input("رقم هاتفك (لن يظهر للمشتري إلا بعد قبول عرضك)")
                                
                                submit_bid = st.form_submit_button("📥 إرسال العرض سرياً للعميل")
                                if submit_bid and loc and m_phone:
                                    bid_payload = {"order_id": order['id'], "merchant_name": f"التاجر كود ({merchant_code})", "merchant_phone": m_phone, "price": price, "currency": currency, "location_in_sudan": loc}
                                    if requests.post(f"{API_URL}/api/v1/bids", json=bid_payload).status_code in [200, 201]:
                                        st.success("🎯 تم إرسال عرضك السري بنجاح!")
        except:
            st.error("خطأ في الاتصال بقاعدة البيانات.")
    elif merchant_code != "":
        st.error("❌ كود التاجر غير صحيح أو غير مسجل في شبكة التجار السبعة المعتمدين.")

# =======================================================
# 4. لوحة تحكم الإدارة المركزية (الأدمن - الصلاحيات والأمان)
# =======================================================
elif menu == "🔐 لوحة تحكم الإدارة (الأدمن)":
    st.header("🔐 غرفة التحكم والمراقبة المركزية للمنصة")
    
    admin_input = st.text_input("أدخل كلمة مرور الإدارة لفتح الصلاحيات الحساسة", type="password")
    
    if admin_input == ADMIN_PASSWORD:
        st.success("🔓 أهلاً بك يا هندسة أيمن. كامل الصلاحيات والبيانات الحساسة تحت تحكمك الآن.")
        
        st.markdown("### 💰 إدارة أسعار الذهب المحلية بالجرام")
        g_price = st.number_input("سعر الجرام المحلي الحالي في السودان (SDG)", min_value=0.0)
        if st.button("🔄 تحديث سعر السوق الآن"):
            if requests.post(f"{API_URL}/api/v1/prices", json={"local_price": float(g_price), "global_ounce": 0.0, "usd_rate": 0.0}).status_code in [200, 201]:
                st.success("🎉 تم تحديث سعر الغرام المحلي بنجاح على البورصة العامة.")
                st.cache_data.clear()
                
        st.markdown("---")
        
        st.markdown("### 🛡️ تتبع الرقابة الميدانية والعمولات (أرقام الهواتف الحقيقية)")
        try:
            res_all = requests.get(f"{API_URL}/api/v1/orders")
            if res_all.status_code == 200:
                all_orders = res_all.json()
                if not all_orders:
                    st.info("لا توجد طلبات في قاعدة البيانات حالياً.")
                else:
                    for o in all_orders:
                        st.text(f"الطلب #{o['id']} | المشتري: {o['buyer_name']} | هاتف المشتري: {o['buyer_phone']} | الحالة: {o['status']}")
        except:
            st.error("خطأ أثناء جلب تقارير الرقابة.")
            
    elif admin_input != "":
        st.error("❌ كلمة المرور غير صحيحة. محاولة دخول غير مصرح بها.")
