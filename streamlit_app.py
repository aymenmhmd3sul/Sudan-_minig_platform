import streamlit as st
import requests

# 1. إعداد الصفحة وتفعيل المحاذاة لليمين (RTL) لدعم اللغة العربية بشكل احترافي على الهاتف
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

st.markdown("""
    <style>
    /* قلب اتجاه الواجهة بالكامل لليمين */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stMarkdownContainer"] p {
        text-align: right;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        direction: RTL;
        text-align: right;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        direction: RTL;
        text-align: right;
    }
    
    /* 🔥 إخفاء الهيدر الافتراضي، أزرار القائمة، وحاوية التنقل العمودية المتداخلة نهائياً وبلا أثر */
    [data-testid="stHeader"], 
    .stAppHeader, 
    [data-testid="stSidebarCollapse"], 
    [data-testid="stSidebarNav"], 
    [data-testid="stSidebarNavItems"],
    section[data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
    }
    
    /* تحسين تباعد الأسطر للعنوان الرئيسي على الجوال ليظهر بشكل مريح */
    h1, h2, h3 {
        line-height: 1.5 !important;
        padding-top: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# رابط السيرفر الخلفي على ريندر
API_URL = "https://sudan-mining-platform.onrender.com"

# =========================================================================
# طبقة جلب البيانات والمؤشرات الذكية
# =========================================================================
@st.cache_data(ttl=20)
def fetch_platform_metrics():
    metrics = {
        "merchants_count": 7, 
        "light_equipment": 27, 
        "heavy_equipment": 14, 
        "generators": 9,      
        "logistics": 22,      
        "gold_price": "في انتظار التحديث"
    }
    try:
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices:
                metrics["gold_price"] = f"{prices[-1].get('price_sdg', 'في انتظار التحديث')}"
    except:
        pass
    return metrics

platform_stats = fetch_platform_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - منظومة الإمداد اللوجستي")
st.markdown("---")

# القائمة الجانبية
menu = st.sidebar.radio(
    "📁 تصفح أقسام المنصة",
    [
        "📊 إحصائيات السوق الحية",
        "👤 اطلب معدة أو خدمة (للمشترين)",
        "🏪 مخزن طلبات الشراء (للتجار المعتمدين)",
        "🗺️ مواقع التعدين وبورصة الذهب"
    ]
)

# =========================================================================
# 1. إحصائيات السوق العامة
# =========================================================================
if menu == "📊 إحصائيات السوق الحية":
    st.header("📈 حجم النشاط والقدرة الاستيعابية للسوق")
    st.write("شبكة ربط لوجستية مغلقة تجمع كبار مستثمري التعدين بأكبر مزودي الخدمات وموردي المعدات في السودان.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏪 شبكة كبار التجار المعتمدين", value=f"{platform_stats['merchants_count']} تجار رئيسيين")
    col2.metric(label="⚙️ إجمالي المواد والخدمات الجاهزة", value="جاهزة للتلبية")
    col3.metric(label="💰 سعر جرام الذهب العالمي الحالي", value=platform_stats['gold_price'])
    
    st.markdown("### 🚜 المنظومة اللوجستية المتوفرة حالياً في المخازن:")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"⚙️ معدات خفيفة\n المتوفر: {platform_stats['light_equipment']} وحدة")
    c2.info(f"🚜 آليات ثقيلة\n المتوفر: {platform_stats['heavy_equipment']} معدة")
    c3.info(f"⚡ طاقة ومولدات\n المتوفر: {platform_stats['generators']} وحدة")
    c4.info(f"💧 خدمات وتموين\n المتوفر: {platform_stats['logistics']} آلية/خدمة")
    
    st.markdown("---")
    st.markdown("> 💡 **ملحوظة:** حدد طلبك ومواصفاتك وسيوصلك العرض الأنسب مباشرة برابط خاص ومشفر يحفظ سرية التعامل والأسعار.")

# =========================================================================
# 2. بوابة المشتري
# =========================================================================
elif menu == "👤 اطلب معدة أو خدمة (للمشترين)":
    st.header("👤 اطلب معدتك أو خدمتك اللوجستية مجاناً")
    st.write("أدخل تفاصيل خط الإنتاج، الآلية المطلوبة بدقة، وسيقوم الموردون بتقديم عروضهم إليك سرياً وبأفضل سعر منافس.")
    
    if "last_order_id" not in st.session_state:
        st.session_state.last_order_id = None
        
    if st.session_state.last_order_id:
        st.success(f"🎉 تم تسجيل طلبك بنجاح برقم آلي مخفي: #{st.session_state.last_order_id}")
        st.info("👇 عروض الأسعار والصور تظهر حية في نفس الصفحة في الأسفل دون حاجة للبحث.")
        
        try:
            res_bids = requests.get(f"{API_URL}/api/v1/bids/order/{st.session_state.last_order_id}", timeout=5)
            if res_bids.status_code == 200:
                bids = res_bids.json()
                if not bids:
                    st.warning("⏳ عروض الأسعار ستظهر هنا فور إرسالها من مخازن التجار سرياً...")
                else:
                    st.markdown(f"### 🎯 العروض المستلمة ({len(bids)} عروض منافسة مخفية الهوية):")
                    for idx, bid in enumerate(bids):
                        with st.container(border=True):
                            col_l, col_r = st.columns([2, 1])
                            with col_l:
                                st.subheader(f"العرض رقم ({idx+1})")
                                st.markdown(f"#### 💰 السعر المعروض: {bid['price']} ({bid.get('currency', 'SDG')})")
                                st.write(f"📍 الموقع الحالي للمعاينة والتسليم: {bid.get('location', 'غير محدد')}")
                                st.write(f"🤝 **التزام العمولة:** {bid.get('commission_status', 'محفوظة للمنصة ومستحقة على التاجر')}")
                                st.caption("🔒 الأسماء والأرقام تظهر أدناه فور ضغط زر الموافقة والاعتماد لحفظ حقوق الأطراف.")
                            with col_r:
                                if bid.get('image_url'):
                                    st.image(bid['image_url'], use_container_width=True)
                                else:
                                    st.info("🖼️ لا توجد صورة مرفقة")
                                    
                            if st.button(f"🤝 الاعتماد الفوري وعرض تقرير سجل التفاوض ({bid['id']})"):
                                requests.put(f"{API_URL}/api/v1/bids/{bid['id']}/accept", timeout=5)
                                st.balloons()
                                st.success("🎉 تم اعتماد العرض بنجاح وإغلاق جلسة المزايدة السيرية.")
                                
                                st.markdown("### 📊 تقرير النظام المعتمد لسجل التفاوض (دليل العمولة والاتفاق):")
                                st.code(f"""
================================================================
⛏️ تقرير نظام المنصة | سجل التفاوض المخفي والاعتماد
================================================================
- معرف الطلب: #{st.session_state.last_order_id} | معرف العرض: #{bid['id']}
- السعر النهائي المرصود: {bid['price']} {bid.get('currency', 'SDG')}
- موقع التسليم والتشغيل الميداني: {bid.get('location', 'موقع التاجر المعتمد')}
----------------------------------------------------------------
[حساب تحصيل عمولة المنصة بالتراضي - مستحقة على التاجر المورد]
- بنك الخرطوم (بنكك): 9291029 (أيمن محمد سليمان)
- هاتف تأكيد الدفع وإرسال إشعار الواتساب: 0912236979
----------------------------------------------------------------
يستخدم هذا السجل اللوجستي كتقرير رسمي لإثبات التوافق وضمان دفع العمولة.
================================================================
""", language="text")
        except:
            st.error("⚠️ خطأ في جلب البيانات")
            
        if st.button("🔄 تقديم طلب شراء جديد لآلية أو خدمة أخرى"):
            st.session_state.last_order_id = None
            st.rerun()
            
    else:
        with st.form("order_form"):
            buyer_name = st.text_input("📝 اسم المشترك (الشخص أو الشركة) - سري")
            buyer_contact = st.text_input("📞 رقم الواتساب أو البريد الإلكتروني")
            
            eq_type = st.selectbox(
                "🚜 فئة المعدة أو الخدمة المطلوبة:",
                [
                    "⚙️ معدات خفيفة وأدوات إنتاج (دقاقات، طواحين، أدوات حفر خفيفة)",
                    "🚜 آليات ومعدات ثقيلة (حفارات، بوكلينات، لودرات، شاحنات)",
                    "⚡ طاقة ومولدات كهرباء (بمختلف السعات والكابلات)",
                    "💧 خدمات وتموين لوجستي (تناكر مياه، ترحيل، إعاشة)",
                    "⛏️ آبار ومواقع تعدين وخطوط إنتاج سيانيد كاملة",
                    "✨ أخرى / صنف غير مدرج في القائمة"
                ]
            )
            
            custom_type = st.text_input("✍️ إذا اخترت أخرى، اكتب اسم المعدة أو الخدمة المطلوبة هنا:")
            required_currency = st.selectbox("💵 العملة المفضلة للسداد وضبط الصفقة:", ["جنيه سوداني (SDG)", "ريال سعودي (SAR)", "دولار أمريكي (USD)"])
            order_location = st.text_input("📍 منطقة التعدين المستهدفة للطلب (مثال: أبو حمد، العبيدية، دلقو)")
            specs = st.text_area("📋 المواصفات الفنية المطلوبة وموقع التشغيل المتوقع:")
            
            submit = st.form_submit_button("🚀 تعميم الطلب في غرف الموردين")
            if submit:
                if (buyer_name) and (buyer_contact) and specs:
                    final_type = custom_type if eq_type == "✨ أخرى / صنف غير مدرج في القائمة" else eq_type
                    payload = {
                        "buyer_name": buyer_name,
                        "buyer_phone": buyer_contact,
                        "equipment_type": final_type,
                        "specifications": f"المنطقة المستهدفة: {order_location} | العملة المطلوبة: {required_currency} | التفاصيل: {specs}"
                    }
                    try:
                        res = requests.post(f"{API_URL}/api/v1/orders", json=payload, timeout=5)
                        if res.status_code in [200, 201]:
                            st.session_state.last_order_id = res.json().get('id')
                            st.rerun()
                        else:
                            st.error("⚠️ السيرفر غير مستجيب")
                    except:
                        st.error("⚠️ خطأ في الاتصال")
                else:
                    st.warning("⚠️ الحقول أساسية (الاسم، وسيلة التواصل، والمواصفات).")

# =========================================================================
# 3. بوابة التجار
# =========================================================================
elif menu == "🏪 مخزن طلبات الشراء (للتجار المعتمدين)":
    st.header("🏪 لوحة تحكم التجار المعتمدين")
    st.write("شارك الحصرية سرياً واعرض صور معداتك وموقعها بناءً على طلب المشتري لضمان عدم حرق الأسعار.")
    
    try:
        res_orders = requests.get(f"{API_URL}/api/v1/orders", timeout=5)
        if res_orders.status_code == 200:
            orders = [o for o in res_orders.json() if o.get('status') != 'completed']
            if not orders:
                st.info("📦 لا توجد طلبات شراء نشطة من الزبائن حالياً.")
            else:
                for order in orders:
                    with st.expander(f"📋 طلب آلية/خدمة مطلوبة - معرف الطلب #{order['id']}"):
                        st.markdown(f"**📑 تفاصيل الاحتياج وموقع الطلب:**\n {order['specifications']}")
                        st.write(f"📅 **تاريخ الطلب:** {order['created_at']}")
                        st.markdown("---")
                        
                        with st.form(f"bid_form_{order['id']}"):
                            m_name = st.selectbox("👤 اسم التاجر/المخزن المورد:", ["مخزن المعدات الخفيفة 1", "مخزن الطاقة والمولدات", "مخزن الآليات الثقيلة", "مخزن الخدمات والتموين"])
                            m_phone = st.text_input("📞 رقم هاتف التاجر (سري - يظهر للمشتري عند الاعتماد)")
                            price = st.number_input("💰 السعر المعروض للبيع أو الإيجار الحالي:", min_value=0)
                            currency = st.selectbox("💵 عملة العرض الفعلي:", ["جنيه سوداني (SDG)", "ريال سعودي (SAR)", "دولار أمريكي (USD)"])
                            loc = st.text_input("📍 الموقع الحالي للمعدة في السودان")
                            img = st.text_input("🖼️ رابط صورة المعدة أو حالتها البصرية (إن وجد)")
                            
                            st.caption("📝 إرسالك للعرض يمثل التزاماً تاماً وموثقاً بسداد عمولة المنصة المحددة بالتراضي إلى حساب الأستاذ أيمن محمد سليمان فور إغلاق الصفقة.")
                            
                            submit_bid = st.form_submit_button("🎯 إرسال العرض سرياً للمشتري")
                            if submit_bid:
                                if m_phone and loc and price > 0:
                                    bid_payload = {
                                        "order_id": order['id'],
                                        "merchant_name": m_name,
                                        "merchant_phone": m_phone,
                                        "price": price,
                                        "currency": currency,
                                        "location": loc,
                                        "image_url": img
                                    }
                                    if requests.post(f"{API_URL}/api/v1/bids", json=bid_payload, timeout=5).status_code in [200, 201]:
                                        st.success("🎯 تم إرسال عرضك المنافس بنجاح وبشكل سري.")
                                else:
                                    st.warning("⚠️ الحقول الأساسية مطلوبة لإتمام المزايدة.")
    except:
        st.error("⚠️ خطأ في الاتصال بالمنصة الخلفية")

# =========================================================================
# 4. إدارة المواقع والأسعار
# =========================================================================
elif menu == "🗺️ مواقع التعدين وبورصة الذهب":
    st.header("🗺️ إدارة المواقع وتحديث أسعار السوق")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("➕ إضافة موقع تعدين أو إنتاج")
        s_name = st.text_input("📌 اسم موقع التعدين الجديد:")
        s_state = st.text_input("📍 الولاية / المنطقة التابعة لها:")
        if st.button("💾 حفظ الموقع الميداني"):
            if s_name and s_state:
                if requests.post(f"{API_URL}/api/v1/sites", json={"name": s_name, "state": s_state}, timeout=5).status_code in [200, 201]:
                    st.success("✔️ تم الحفظ بنجاح في قاعدة البيانات.")
                    
    with col_b:
        st.subheader("💰 تحديث بورصة أسعار الذهب اللحظية والمحلية")
        gold_region = st.text_input("📍 المنطقة الخاصة بالتسعير المحلي:")
        g_price = st.number_input("💵 سعر الجرام الحالي بالمنطقة (ج.س):", min_value=0)
        if st.button("🔄 تحديث السعر والبورصة الآن"):
            if gold_region and g_price > 0:
                payload_price = {"price_sdg": f"جرام عيار 21 في {gold_region}: {g_price} ج.س"}
                if requests.post(f"{API_URL}/api/v1/prices", json=payload_price, timeout=5).status_code in [200, 201]:
                    st.success("🎉 تم تحديث البورصة حية في لوحة المؤشرات.")
                    st.cache_data.clear()
