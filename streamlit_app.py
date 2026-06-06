import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

# رابط السيرفر الفعلي المرفوع على Render
API_URL = "https://sudan-mining-platform.onrender.com"

# ==========================================
# طبقة جلب البيانات (Data Layer & Caching)
# ==========================================

@st.cache_data(ttl=30)  # كاش لمدة 30 ثانية لتحديث البيانات بسلاسة
def fetch_dashboard_metrics():
    """جلب المؤشرات الخمسة الأساسية من الـ API بشكل حي ومعالجة الجداول الفارغة"""
    metrics = {
        "sites_count": 0,
        "equipment_count": 0,
        "reports_count": 0,
        "total_production": 0.0,
        "gold_price": "في انتظار التحديث"
    }
    
    try:
        # 1. جلب المواقع
        r_sites = requests.get(f"{API_URL}/api/v1/sites", timeout=5)
        if r_sites.status_code == 200:
            metrics["sites_count"] = len(r_sites.json())
            
        # 2. جلب المعدات
        r_eq = requests.get(f"{API_URL}/api/v1/equipment", timeout=5)
        if r_eq.status_code == 200:
            metrics["equipment_count"] = len(r_eq.json())
            
        # 3. جلب البلاغات
        r_rep = requests.get(f"{API_URL}/api/v1/reports", timeout=5)
        if r_rep.status_code == 200:
            metrics["reports_count"] = len(r_rep.json())
            
        # 4. جلب وحساب إجمالي الإنتاج
        r_prod = requests.get(f"{API_URL}/api/v1/production", timeout=5)
        if r_prod.status_code == 200:
            productions = r_prod.json()
            if productions:
                metrics["total_production"] = sum(item.get("amount", 0) for item in productions)
            
        # 5. جلب آخر سعر للذهب
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices and len(prices) > 0:
                metrics["gold_price"] = f"{prices[-1].get('price', 0):,} ج.س"
    except Exception as e:
        pass  # الاحتفاظ بالقيم الافتراضية بدلاً من انهيار الواجهة
        
    return metrics

# جلب البيانات الحية لبدء تشغيل اللوحة
live_data = fetch_dashboard_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - Sudan Mining Hub")
st.markdown("---")

# القائمة الجانبية لكافة أقسام المنصة
menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 لوحة المؤشرات (المستثمرين)",
        "🚜 تتبع المعدات والآليات",
        "🗺️ مواقع التعدين",
        "💰 تحديث بورصة الأسعار",
        "📝 تسجيل حساب جديد"
    ]
)

# ==========================================
# 1. لوحة المؤشرات (القسم الرئيسي للمستثمرين)
# ==========================================
if menu == "📊 لوحة المؤشرات (المستثمرين)":
    st.header("📈 لوحة الأداء العام والمؤشرات الاستثمارية")
    st.write("نظام سحابي متكامل لتتبع وإدارة عمليات ومواقع التعدين، الآليات، والإنتاج الحي في السودان.")
    
    st.markdown("### 🏷️ المؤشرات الحية للمنصة (من واقع قاعدة البيانات)")
    
    # توزيع المؤشرات الخمسة الاستثمارية في مربعات رقمية جذابة
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric(label="🗺️ مواقع التعدين النشطة", value=f"{live_data['sites_count']} موقع")
    col2.metric(label="🚜 المعدات المسجلة", value=f"{live_data['equipment_count']} آلية")
    col3.metric(label="🚨 البلاغات المفتوحة", value=f"{live_data['reports_count']} بلاغ")
    col4.metric(label="🏆 إجمالي إنتاج الذهب", value=f"{live_data['total_production']} جرام")
    col5.metric(label="💰 سعر الخام الحالي", value=live_data['gold_price'])

    st.markdown("---")
    st.info("💡 هذه اللوحة تحدث بياناتها تلقائياً من خادم PostgreSQL السحابي لتقديم رؤية دقيقة للشركاء والمستثمرين.")

# ==========================================
# 2. قسم المعدات والآليات
# ==========================================
elif menu == "🚜 تتبع المعدات والآليات":
    st.header("🚜 إدارة وتتبع الآليات والمعدات")
    st.write("يمكنك مراقبة الوقود، ساعات العمل، ومواقع الجرافات والمولدات في البيئة الحية.")
    
    st.subheader("➕ إضافة معدة جديدة للموقع")
    eq_name = st.text_input("اسم المعدة / الآلية")
    eq_type = st.selectbox("نوع المعدة", ["مولد كهربائي", "جرافة (Digger)", "مضخة مياه"])
    
    if st.button("حفظ المعدة"):
        if eq_name:
            payload = {"name": eq_name, "type": eq_type, "status": "active"}
            try:
                res = requests.post(f"{API_URL}/api/v1/equipment", json=payload, timeout=5)
                if res.status_code in [200, 201]:
                    st.success(f"✔️ تم تسجيل {eq_name} بنجاح في قاعدة البيانات!")
                    st.cache_data.clear() # تفريغ الكاش لتحديث الأرقام فوراً
                else:
                    st.error(f"خطأ من السيرفر: {res.status_code}")
            except Exception as e:
                st.error("❌ فشل الاتصال بالسيرفر لإضافة المعدة.")
        else:
            st.warning("الرجاء إدخال اسم المعدة أولاً.")

# ==========================================
# 3. قسم مواقع التعدين
# ==========================================
elif menu == "🗺️ مواقع التعدين":
    st.header("🗺️ تتبع مواقع التعدين والامتياز")
    st.subheader("➕ تسجيل موقع تعدين جديد")
    site_name = st.text_input("اسم موقع التعدين")
    site_state = st.text_input("الولاية / المنطقة")
    
    if st.button("حفظ الموقع"):
        if site_name and site_state:
            payload = {"name": site_name, "state": site_state, "coordinates": "0.0, 0.0", "is_active": True}
            try:
                res = requests.post(f"{API_URL}/api/v1/sites", json=payload, timeout=5)
                if res.status_code in [200, 201]:
                    st.success(f"✔️ تم تسجيل موقع {site_name} بنجاح!")
                    st.cache_data.clear()
                else:
                    st.error(f"خطأ: {res.status_code}")
            except Exception as e:
                st.error("❌ فشل الاتصال بالخادم السحابي.")

# ==========================================
# 4. لوحة التشغيل وضخ الأسعار (التغذية التشغيلية)
# ==========================================
elif menu == "💰 تحديث بورصة الأسعار":
    st.header("💰 الإدارة التشغيلية لبورصة أسعار الذهب")
    st.write("تحديث أسعار جرام الذهب الخام المعتمدة في السوق المحلي لتعكس حياً في لوحة المستثمرين.")
    
    new_price = st.number_input("سعر جرام الذهب الحالي (بالجنيه السوداني)", min_value=1000, value=95000, step=500)
    
    if st.button("تحديث وضخ السعر الآن"):
        payload = {"price": float(new_price), "currency": "SDG"}
        try:
            res = requests.post(f"{API_URL}/api/v1/prices", json=payload, timeout=5)
            if res.status_code in [200, 201]:
                st.success(f"🎉 تم ضخ السعر بنجاح ({new_price:,} ج.س) وتحديث قاعدة بيانات PostgreSQL!")
                st.cache_data.clear()
            else:
                st.error(f"فشل التحديث: {res.status_code}")
        except Exception as e:
            st.error("🚨 خطأ في الاتصال بالـ API.")

# ==========================================
# 5. قسم التسجيل
# ==========================================
elif menu == "📝 تسجيل حساب جديد":
    st.header("📝 إنشاء حساب جديد في المنصة")
    username = st.text_input("اسم المستخدم")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("تنفيذ التسجيل"):
        try:
            response = requests.post(f"{API_URL}/api/v1/users/register", json={"username": username, "email": email, "password": password}, timeout=5)
            if response.status_code in [200, 201]:
                st.success("🎉 تم إنشاء الحساب بنجاح!")
            else:
                st.error(f"خطأ: {response.json().get('detail', 'تعذر التسجيل')}")
        except Exception as e:
            st.error("🚨 خطأ في الاتصال بالخادم.")
