import streamlit as st
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="كافي أونلاين - حاسبة التكلفة", page_icon="🛍️", layout="centered")

# --- الثوابت وإعدادات العملة ---
EXCHANGE_RATE_SAR_TO_YER = 445.0  # سعر صرف الريال السعودي مقابل اليمني
SHIPPING_FEE_SAR = 18.75           # الشحن التقديري بالريال السعودي
SERVICE_FEE_PERCENT = 0.05        # رسوم الخدمة 5%
YOUR_WHATSAPP_NUMBER = "967700000000"  # اكتب رقم الواتساب الخاص بك هنا

st.title("كافي أونلاين 🛍️")
st.subheader("حاسبة تكلفة الطلب من الخارج")

# تنبيه مناطق التوصيل
st.info("📍 **مناطق التوصيل المتاحة حالياً:** حضرموت - عدن فقط.")

st.write("أدخل رابط المنتج وسعره بالريال السعودي لحساب التكلفة التقديرية بالريال اليمني.")

# --- واجهة المستخدم ---
product_url = st.text_input("رابط المنتج", placeholder="https://www.shein.com/...")

with st.form("calc_form"):
    city = st.selectbox("اختر مدينة التوصيل", ["حضرموت", "عدن"])
    price_sar = st.number_input(
        "سعر المنتج بالريال السعودي (SAR)", 
        min_value=0.0, 
        value=0.0, 
        step=1.0, 
        format="%.2f"
    )
    submitted = st.form_submit_button("احسب التكلفة")

if submitted:
    if price_sar <= 0:
        st.error("يرجى إدخال سعر المنتج بشكل صحيح.")
    else:
        service_fee_sar = price_sar * SERVICE_FEE_PERCENT
        total_sar = price_sar + SHIPPING_FEE_SAR + service_fee_sar
        total_yer = total_sar * EXCHANGE_RATE_SAR_TO_YER
        
        st.success("تم حساب التكلفة بنجاح!")
        st.markdown(f"### 💵 التكلفة الإجمالية: **{total_yer:,.0f} ريال يمني**")
        
        st.write("---")
        st.write("**تفاصيل الحساب:**")
        st.write(f"- مدينة التوصيل: `{city}`")
        st.write(f"- سعر المنتج: `{price_sar:.2f} ر.س`")
        st.write(f"- الشحن التقديري: `{SHIPPING_FEE_SAR:.2f} ر.س`")
        st.write(f"- رسوم الخدمة (5%): `{service_fee_sar:.2f} ر.س`")
        st.write(f"- سعر صرف الريال السعودي: `{EXCHANGE_RATE_SAR_TO_YER:,.0f} ر.ي`")
        
        st.warning("🛡️ **ضمان كافي أونلاين:** إذا لم تصلك شحنتك لأي سبب، نضمن لك استرجاع أموالك بالكامل.")
        
        msg = f"السلام عليكم، أرغب بطلب المنتج التالي عبر كافي أونلاين:\n"
        msg += f"📍 المدينة: {city}\n"
        if product_url:
            msg += f"🔗 الرابط: {product_url}\n"
        msg += f"💰 السعر بالريال السعودي: {price_sar:.2f} ر.س\n"
        msg += f"🇾🇪 التكلفة الإجمالية المقدرة: {total_yer:,.0f} ريال يمني"
        
        whatsapp_url = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display:inline-block; background-color:#25D366; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-weight:bold;">📲 إرسال الطلب عبر الواتساب</a>', unsafe_allowed_html=True)

st.write("---")
st.caption(f"التوصيل: حضرموت وعدن • رسوم الخدمة 5% • سعر الصرف {EXCHANGE_RATE_SAR_TO_YER:,.0f} ر.ي")
