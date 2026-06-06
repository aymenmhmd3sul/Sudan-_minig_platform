    
    try:
        res_orders = requests.get(f"{API_URL}/api/v1/orders")
        if res_orders.status_code == 200:
            orders = [o for o in res_orders.json() if o.get("status") == "نشط"]
            
            if not orders:
                st.info("📦 لا توجد طلبات شراء نشطة حالياً من المشترين.")
            else:
                for order in orders:
                    with st.expander(f"📋 طلب رقم #{order['id']} - مطلوب: {order['equipment_type']}"):
                        st.write(f"**المواصفات المطلوبة:** {order['specifications']}")
                        st.write(f"**تاريخ الطلب:** {order['created_at']}")
                        st.markdown("---")
                        st.subheader("📝 تقديم عرض سعر سري لهذا الطلب")
                        
                        # نموذج تقديم العرض داخل الإكسباندر
                        with st.form(f"bid_form_{order['id']}"):
                            merchant_name = st.selectbox("اختر اسمك (التاجر المعتمد)", [f"التاجر المعتمد #{i}" for i in range(1, 8)])
                            merchant_phone = st.text_input("رقم هاتف التاجر الخاص بالصفقة")
                            price = st.number_input("السعر المعروض للبيع", min_value=1.0, step=1000.0)
                            currency = st.selectbox("العملة", ["جنيه سوداني (SDG)", "درهم إماراتي (AED)", "دولار أمريكي (USD)"])
                            location_sudan = st.text_input("موقع المعدة الحالي للمعاينة (مثال: أبو حمد، بربر، الخرطوم)")
                            image_url = st.text_input("رابط صورة المعدة للمعاينة البصرية (أو اتركه فارغاً)")
                            
                            st.caption("ℹ️ ملاحظة: بموجب شروط المنصة، يدفع التاجر عمولة مرنة تتراوح بين 0.5% إلى 2% بعد إتمام عملية البيع للمشتري.")
                            
                            submit_bid = st.form_submit_button("📥 إرسال العرض سرياً للمشتري")
                            
                            if submit_bid:
                                if merchant_phone and location_sudan:
                                    bid_payload = {
                                        "order_id": order['id'],
                                        "merchant_name": merchant_name,
                                        "merchant_phone": merchant_phone,
                                        "price": price,
                                        "currency": currency,
                                        "location_in_sudan": location_sudan,
                                        "image_url": image_url if image_url else None,
                                        "commission_rate": 1.0,
                                        "commission_status": "معلقة"
                                    }
                                    res_bid = requests.post(f"{API_URL}/api/v1/bids", json=bid_payload)
                                    if res_bid.status_code in [200, 201]:
                                        st.success("🎯 تم إرسال عرضك السري بنجاح للمشتري!")
                                    else:
                                        st.error("❌ فشل إرسال العرض، راجع السيرفر.")
                                else:
                                    st.warning("⚠️ يرجى إدخال رقم الهاتف وموقع المعاينة الجغرافي.")
    except Exception as e:
        st.error("❌ فشل الاتصال بقاعدة البيانات لجلب طلبات المشترين.")

# =======================================================
# 4. غرف التفاوض والاتفاق واستخراج الأدلة
# =======================================================
elif menu == "💬 غرف التفاوض والاتفاق":
    st.header("💬 غرف التفاوض الذكية والموافقة على الصفقات")
    st.write("أدخل اسمك كمشتري أو رقم طلبك لاستعراض العروض السرية المقدمة لك من التجار، والتفاوض ومعاينة الصور والمواقع الجغرافية.")
    
    order_id_input = st.number_input("أدخل رقم طلبك (Order ID) لعرض عروض الأسعار المقدمة لك:", min_value=1, step=1)
    
    if order_id_input:
        try:
            res_bids = requests.get(f"{API_URL}/api/v1/bids/order/{order_id_input}")
            if res_bids.status_code == 200:
                bids = res_bids.json()
                
                if not bids:
                    st.info("⏳ لم يقم أي تاجر بتقديم عرض على هذا الطلب حتى الآن. العروض تظهر هنا فور إرسالها.")
                else:
                    st.success(f"🎉 تم العثور على ({len(bids)}) عروض سرية مقدمة لطلبك!")
                    
                    for idx, bid in enumerate(bids):
                        st.markdown(f"### 📦 العرض المتاح رقم {idx+1}")
                        
                        col_left, col_right = st.columns([2, 1])
                        
                        with col_left:
                            st.write(f"**💰 السعر المعروض:** {bid['price']:,} {bid['currency']}")
                            st.write(f"**📍 موقع المعدة الجغرافي للمعاينة بالسودان:** {bid['location_in_sudan']}")
                            st.write(f"**🤝 التزام العمولة (يدفعها التاجر للمنصة):** {bid['commission_text']}")
                            st.warning("🔒 هوية التاجر ورقم هاتفه مخفيان لحماية حقوق المنصة وتجنب البيع الخارجي.")
                        
                        with col_right:
                            if bid.get('image_url'):
                                st.image(bid['image_url'], caption="صورة المعدة المرفوعة من مخزن التاجر الافتراضي", use_container_width=True)
                            else:
                                st.info("🖼️ لا توجد صورة مرفقة مع هذا العرض.")
                        
                        # زر القبول والاتفاق الرسمي لتوليد سجل المراسلات كدليل للعمولة
                        if st.button(f"🤝 قبول هذا العرض والاتفاق الرسمي (عرض رقم #{bid['id']})"):
                            # 1. تحديث حالة الطلب إلى تم الاتفاق
                            requests.put(f"{API_URL}/api/v1/orders/{order_id_input}/status?status=تم الاتفاق مع {bid['merchant_name']}")
                            
                            st.balloons()
                            st.success("🎉 مبروك! تم إتمام الاتفاق برغبتك الحرة بالكامل.")
                            
                            # كشف الهويات والأرقام بعد الضغط بشكل آمن
                            st.markdown("#### 📱 بيانات التواصل المباشر للمعاينة والتسليم:")
                            st.info(f"📞 **رقم هاتف التاجر (البائع الملتزم بالعمولة):** {bid['merchant_phone']}")
                            
                            # استخراج سجل المراسلات الموقّع كدليل قانوني وإداري للمنصة
                            st.markdown("#### 📝 سجل المراسلات المستخرج كدليل (رسمي للمنصة):")
                            evidence_text = f"""
                            ------------------------------------------
                            📄 دليل اتفاق منصة تعدين السودان الرقمية
                            ------------------------------------------
                            - رقم طلب الشراء: {order_id_input}
                            - رقم العرض المقبول: {bid['id']}
                            - السعر المتفق عليه برغبة الطرفين: {bid['price']:,} {bid['currency']}
                            - موقع المعدة للمعاينة والتسليم: {bid['location_in_sudan']}
                            - الطرف الملزم بدفع العمولة: التاجر ({bid['merchant_name']})
                            - نسبة العمولة المعتمدة: {bid['commission_rate']}%
                            - حالة العمولة الحالية: قيد الدفع بعد الفحص والاستلام الميداني
                            - تاريخ وتوقيت العملية الآلي: {bid['created_at']}
                            ------------------------------------------
                            تنبيه: هذا السجل مستخرج برمجياً ومحفوظ في السيرفر لضمان حق المنصة في العمولة التي يدفعها التاجر الملتزم.
                            """
                            st.code(evidence_text, language="text")
                            st.info("💡 تم حفظ هذا السجل تلقائياً، يرجى التواصل مع التاجر على الرقم أعلاه لترتيب المعاينة الميدانية بـأبو حمد أو موقعها الجغرافي.")
                        st.markdown("---")
        except Exception as e:
            st.error("❌ خطأ أثناء جلب العروض من السيرفر.")

# =======================================================
# 5. قسم مواقع التعدين (الأصلية)
# =======================================================
elif menu == "🗺️ مواقع التعدين":
    st.header("🗺️ تتبع مواقع التعدين والامتياز")
    st.subheader("➕ تسجيل موقع تعدين جديد")
    site_name = st.text_input("اسم موقع التعدين")
    site_state = st.text_input("الولاية / المنطقة")
    
    if st.button("💾 حفظ الموقع"):
        if site_name and site_state:
            payload = {"name": site_name, "state": site_state, "is_active": True}
            try:
                res = requests.post(f"{API_URL}/api/v1/sites", json=payload)
                if res.status_code in [200, 201]:
                    st.success(f"✔️ تم تسجيل موقع {site_name} بنجاح في قاعدة البيانات.")
                    st.cache_data.clear()  # تفريغ الكاش لتحديث الأرقام فوراً
                else:
                    st.error(f"❌ خطأ من السيرفر: {res.status_code}")
            except Exception as e:
                st.error("❌ فشل الاتصال بالخادم السحابي.")
        else:
            st.warning("⚠️ الرجاء إدخال اسم الموقع والولاية أولاً.")

# =======================================================
# 6. قسم تحديث بورصة الأسعار (الأصلية)
# =======================================================
elif menu == "💰 تحديث بورصة الأسعار":
    st.header("💰 الإدارة التشغيلية لبورصة أسعار الذهب")
    st.write("تحديث أسعار الذهب الخام المعتمدة في السوق المحلي لتنعكس حية في لوحة المستثمرين.")
    
    new_price = st.number_input("سعر جرام الذهب الحالي (بالجنيه السوداني)", min_value=0.0, step=100.0)
    
    if st.button("🔄 تحديث وضع السعر الآن"):
        payload = {"local_price": float(new_price), "global_ounce": 0.0, "usd_rate": 0.0}
        try:
            res = requests.post(f"{API_URL}/api/v1/prices", json=payload)
            if res.status_code in [200, 201]:
                st.success(f"🎉 تم تحديث قاعدة بيانات الأسعار بنجاح إلى: {new_price:,} ج.س")
                st.cache_data.clear()
            else:
                st.error(f"❌ فشل التحديث: {res.status_code}")
        except Exception as e:
            st.error("❌ خطأ في الاتصال بالـ API.")

# =======================================================
# 7. قسم تسجيل حساب جديد (الأصلية)
# =======================================================
elif menu == "📝 تسجيل حساب جديد":
    st.header("📝 إنشاء حساب جديد في المنصة")
    username = st.text_input("اسم المستخدم")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("🚀 تنفيذ التسجيل"):
        try:
            response = requests.post(f"{API_URL}/api/v1/users/register", json={"username": username, "email": email, "password": password})
            if response.status_code in [200, 201]:
                st.success("🎉 تم إنشاء الحساب بنجاح!")
            else:
                st.error(f"❌ خطأ: {response.json().get('detail', 'فشل التسجيل')}")
        except Exception as e:
            st.error("❌ خطأ في الاتصال بالخادم.")
