import streamlit as st
st.set_page_config(page_title='منصة تعدين السودان الرقمية', layout='wide')
st.sidebar.title('📌 القائمة الرئيسية')
page = st.sidebar.radio('التنقل', ['📊 الداشبورد', '🛒 المشتري', '🏪 التاجر', '🤝 الصفقات', '⚙️ النظام'])
if page == '📊 الداشبورد':
    st.title('📊 الداشبورد')
    st.success('النظام يعمل بشكل طبيعي')
elif page == '🛒 المشتري':
    st.title('🛒 المشتري')
    st.selectbox('نوع الطلب', ['معدات خفيفة', 'معدات ثقيلة'])
elif page == '🏪 التاجر':
    st.title('🏪 التاجر')
elif page == '🤝 الصفقات':
    st.title('🤝 الصفقات')
elif page == '⚙️ النظام':
    st.title('⚙️ معلومات النظام')
    st.info('النظام يعمل بشكل مستقر')
