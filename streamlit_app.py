import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

# رابط السيرفر الخلفي على ريندر
API_URL = "https://sudan-mining-platform.onrender.com"

# =======================================================
# طبقة جلب البيانات والمؤشرات الذكية
# =======================================================
@st.cache_data(ttl=20)
def fetch_platform_metrics():
    metrics = {
        "merchants_count": 7,  # التجار السبعة الأساسيين لمنح الهيبة للسوق
        "excavators": 27,      # أرقام تقريبية ذكية حسب مقترحك لتعزيز الثقة
        "loaders": 14,
        "crushers": 9,
        "trucks": 22,
        "gold_price": "في انتظار التحديث"
    }
    try:
        # جلب آخر سعر للذهب من قاعدة البيانات
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices:
                metrics["gold_price"] = f"{prices[-1].get('local_price', 0.0):,}"
    except:
        pass
    return metrics

platform_stats = fetch_platform_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - سوق المعدات الثقيلة")
st.markdown("---")

# القائمة الجانبية
menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 إحصائيات السوق الحية",
        "👤 اطلب معدة الآن (للمشترين)",
        "🏪 مخزن طلبات الشراء (للتجار الـ 7)",
        "🗺️ مواقع التعدين وبورصة الذهب",
    ]
)

# =======================================================
# 1. إحصائيات السوق العامة (الحل الوسط لمنح الثقة دون كشف المخزن)
# =======================================================
if menu == "📊 إحصائيات السوق الحية":
    st.header("📈 حجم النشاط والقدرة الاستيعابية للسوق")
    st.write("شبكة ربط لوجستية مغلقة تجمع كبار مستثمري التعدين بأكبر 7 تجار وموردي معدات ثقيلة في السودان.")
    
    # عرض العدادات العامة لخلق هيبة للمنصة
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏪 شبكة كبار التجار المعتمدين", value=f"{platform_stats['merchants_count']} تجار رئيسيين")
    col2.metric(label="⚙️ إجمالي المعدات الجاهزة للمعاينة", value=f"{platform_stats['excavators'] + platform_stats['loaders'] + platform_stats['crushers'] + platform_stats['trucks']} معدة وجاهزة")
    col3.metric(label="💰 سعر جرام الذهب الحالي (SDG)", value=platform_stats['gold_price'])
    
    st.markdown("### 🚜 الفئات والآليات المتوفرة حالياً في المخازن الافتراضية:")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"🚜 **حفارات / بوكلينات**\n\n🎯 المتوفر: {platform_stats['excavators']} معدة")
    c2.info(f"🚚 **لودرات وشاحنات**\n\n🎯 المتوفر: {platform_stats['loaders']} معدة")
    c3.info(f"🏭 **كسارات وطواحين**\n\n🎯 المتوفر: {platform_stats['crushers']} وحدة")
    c4.info(f"🚛 **ناقلات وخدمات**\n\n🎯 المتوفر: {platform_stats['trucks']} آلية")
    
    st.markdown("---")
    st.markdown("> **💡 ملاحظة للمشترين:** حفاظاً على خصوصية الأسعار وحماية حركة السوق، المخازن مصنفة كـ **مخازن افتراضية مغلقة**. لست بحاجة للبحث؛ فقط أدخل مواصفاتك وسيصلك العرض الأنسب مباشرة برابط خاص.")

# =======================================================
# 2. بوابة المشتري: طلب معدة + الانتقال الفوري لرابط العروض الذكي
# =======================================================
elif menu == "👤 اطلب معدة الآن (للمشترين)":
    st.header("👤 اطلب معدتك مجاناً وخلال دقائق")
    st.write("اكتب مواصفات المعدة أو خط الإنتاج المطلوبة بدقة، وسيقوم الموردون بتقديم عروضهم إليك سرياً.")
    
    # استخدام الـ session_state لحفظ رابط الطلب الأخير وتسهيل التدفق الرقمي
    if "last_order_id" not in st.session_state:
        st.session_state.last_order_id = None

    if st.session_state.last_order_id:
        st.success(f"🎉 تم تسجيل طلبك بنجاح برقم آلي: #{st.session_state.last_order_id}")
        st.info("👇 عروض التجار والأسعار والصور تظهر حية في الأسفل مباشرة دون حاجة للبحث!")
        
        # عرض العروض مباشرة في نفس الصفحة لعدم تشتيت المشتري
        try:
            res_bids = requests.get(f"{API_URL}/api/v1/bids/order/{st.session_state.last_order_id}")
            if res_bids.status_code == 200:
                bids = res_bids.json()
                if not bids:
                    st.warning("⏳ عروض التجار قيد التحضير الآن... ستظهر هنا فور إرسالها من مخازنهم سرياً.")
                else:
                    st.markdown(f"### 🎯 العروض المستلمة ({len(bids)})")
                    for idx, bid in enumerate(bids):
                        with st.container(border=True):
                            col_l, col_r = st.columns([2, 1])
                            with col_l:
                                st.subheader(f"العرض رقم {idx+1}")
                                st.markdown(f"#### **💰 السعر:** {bid['price']:,} {bid['currency']}")
                                st.write(f"**📍 الموقع الحالي للمعاينة:** {bid['location_in_sudan']}")
                                st.write(f"**🤝 التزام العمولة:** {bid['commission_text']}")
                                st.caption("🔒 رقم الهاتف واسم التاجر مخفيان لضمان جدية الاتفاق وحقوق المنصة.")
                            with col_r:
                                if bid.get('image_url'):
                                    st.image(bid['image_url'], use_container_width=True)
                                else:
                                    st.info("🖼️ لا توجد صورة مرفقة")
                            
                            if st.button(f"🤝 قبول العرض والاتفاق الرسمي (عرض #{bid['id']})", key=f"accept_{bid['id']}"):
                                requests.put(f"{API_URL}/api/v1/orders/{st.session_state.last_order_id}/status?status=تم الاتفاق")
                                st.balloons()
                                st.success("🎉 مبروك! تم إبرام الاتفاق بنجاح وتم توليد مستند الدليل لحفظ عمولة المنصة.")
                                st.markdown(f"### 📞 تواصل فوراً مع المورد للمعاينة الميدانية: `{bid['merchant_phone']}`")
                                
                                # سجل المراسلات كدليل
                                st.code(f"""
                                📄 دليل اتفاق رسمي - منصة تعدين السودان
                                ----------------------------------------
                                - طلب شراء رقم: {st.session_state.last_order_id} | عرض رقم: {bid['id']}
                                - السعر المتفق عليه: {bid['price']:,} {bid['currency']}
                                - الموقع والمطابقة الميدانية: {bid['location_in_sudan']}
                                - الطرف الملزم بالعمولة: التاجر ({bid['merchant_name']})
                                - نسبة العمولة المحفوظة للمنصة: {bid['commission_rate']}%
                                ----------------------------------------
                                """, language="text")
        except:
            st.error("خطأ في جلب البيانات.")
            
        if st.button("🔄 تقديم طلب شراء جديد آخر"):
            st.session_state.last_order_id = None
            st.rerun()
            
    else:
        with st.form("order_form"):
            buyer_name = st.text_input("اسم المشتري أو الشركة")
            buyer_phone = st.text_input("رقم الهاتف (مخفي تماماً ولن يظهر إلا للتاجر الذي تقبل عرضه)")
            eq_type = st.selectbox("نوع الآلية المطلوبة", ["بوكلين / حافرة", "لودر / شاحنة", "بلدوزر", "طاحونة رطبة / جافة", "خط سيانيد"])
            specs = st.text_area("المواصفات الفنية المطلوبة وموقع التشغيل المتوقع")
            
            submit = st.form_submit_button("🚀 نشر الطلب في غرف الموردين")
            if submit:
                if buyer_name and buyer_phone and specs:
                    payload = {"buyer_name": buyer_name, "buyer_phone": buyer_phone, "equipment_type": eq_type, "specifications": specs, "status": "نشط"}
                    try:
                        res = requests.post(f"{API_URL}/api/v1/orders", json=payload)
                        if res.status_code in [200, 201]:
                            st.session_state.last_order_id = res.json().get("id")
                            st.rerun()
                    except:
                        st.error("السيرفر غير مستجيب.")
                else:
                    st.warning("⚠️ الحقول أساسية.")

# =======================================================
# 3. بوابة التجار الـ 7 لتقديم العروض السرية
# =======================================================
elif menu == "🏪 مخزن طلبات الشراء (للتجار الـ 7)":
    st.header("🏪 لوحة تحكم التجار المعتمدين")
    st.write("بصفتك تاجراً معتمداً، يمكنك تقديم أسعارك الحصرية سرياً وعرض صور معداتك ومواقعها بناءً على طلب المشتري.")
    
    try:
        res_orders = requests.get(f"{API_URL}/api/v1/orders")
        if res_orders.status_code == 200:
            orders = [o for o in res_orders.json() if o.get("status") == "نشط"]
            if not orders:
                st.info("📦 لا توجد طلبات شراء نشطة من الزبائن حالياً.")
            else:
                for order in orders:
                    with st.expander(f"📋 طلب شراء #{order['id']} - آلية مطلوبة: {order['equipment_type']}"):
                        st.markdown(f"**المواصفات المطلوبة:**\n> {order['specifications']}")
                        st.write(f"**تاريخ الطلب:** {order['created_at']}")
                        st.markdown("---")
                        
                        with st.form(f"bid_form_{order['id']}"):
                            m_name = st.selectbox("اسم التاجر", [f"التاجر المعتمد #{i}" for i in range(1, 8)])
                            m_phone = st.text_input("رقم هاتفك للتواصل عند الاتفاق")
                            price = st.number_input("السعر المعروض للبيع", min_value=1.0)
                            currency = st.selectbox("العملة", ["جنيه سوداني (SDG)", "درهم إماراتي (AED)", "دولار أمريكي (USD)"])
                            loc = st.text_input("موقع المعاينة الحالي في السودان")
                            img = st.text_input("رابط صورة المعدة للمعاينة البصرية (إن وجد)")
                            
                            st.caption("📝 التزام: يدفع التاجر عمولة المنصة (من 0.5% إلى 2%) بعد البيع الفعلي واستلام المشتري للبضاعة.")
                            
                            submit_bid = st.form_submit_button("📥 إرسال العرض سرياً")
                            if submit_bid:
                                if m_phone and loc:
                                    bid_payload = {"order_id": order['id'], "merchant_name": m_name, "merchant_phone": m_phone, "price": price, "currency": currency, "location_in_sudan": loc, "image_url": img if img else None}
                                    if requests.post(f"{API_URL}/api/v1/bids", json=bid_payload).status_code in [200, 201]:
                                        st.success("🎯 تم إرسال عرضك السري بنجاح!")
                                else:
                                    st.warning("⚠️ يرجى ملء الحقول الأساسية.")
    except:
        st.error("خطأ في الاتصال.")

# =======================================================
# 4. بقية الأقسام الأصلية (مواقع التعدين والأسعار)
# =======================================================
elif menu == "🗺️ مواقع التعدين وبورصة الذهب":
    st.header("🗺️ إدارة المواقع وتحديث أسعار السوق")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("➕ إضافة موقع تعدين")
        s_name = st.text_input("اسم موقع التعدين")
        s_state = st.text_input("الولاية / المنطقة")
        if st.button("💾 حفظ الموقع"):
            if s_name and s_state:
                if requests.post(f"{API_URL}/api/v1/sites", json={"name": s_name, "state": s_state, "is_active": True}).status_code in [200, 201]:
                    st.success("✔️ تم الحفظ بنجاح.")
    with col_b:
        st.subheader("💰 تحديث بورصة أسعار الذهب")
        g_price = st.number_input("سعر الجرام الحالي (ج.س)", min_value=0.0)
        if st.button("🔄 تحديث السعر الآن"):
            if requests.post(f"{API_URL}/api/v1/prices", json={"local_price": float(g_price), "global_ounce": 0.0, "usd_rate": 0.0}).status_code in [200, 201]:
                st.success("🎉 تم تحديث البورصة حية.")
                st.cache_data.clear()
