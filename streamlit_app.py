import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="كافي أونلاين - حاسبة التكلفة", page_icon="🛍️", layout="centered")

# --- الثوابت وإعدادات العملة ---
EXCHANGE_RATE_SAR_TO_YER = 445.0  # سعر صرف الريال السعودي مقابل اليمني
SHIPPING_FEE_SAR = 18.75           # الشحن التقديري بالريال السعودي
SERVICE_FEE_PERCENT = 0.05        # رسوم الخدمة 5%
YOUR_WHATSAPP_NUMBER = "967700000000"  # اكتب رقم الواتساب هنا بالرمز الدولي بدون +

st.title("كافي أونلاين 🛍️")
st.subheader("حاسبة تكلفة الطلب من الخارج")

# تنبيه مناطق التوصيل
st.info("📍 **مناطق التوصيل المتاحة حالياً:** حضرموت - عدن فقط.")

st.write("أدخل رابط المنتج من (SHEIN أو غيره) لجلب بياناته وحساب التكلفة التقديرية بالريال اليمني.")

# --- وظيفة جلب بيانات المنتج والسعر تلقائياً ---
def fetch_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    details = {"title": None, "image": None, "price": None}
    try:
        match = re.search(r'https?://[^\s]+', url)
        clean_url = match.group(0) if match else url
        
        response = requests.get(clean_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. جلب الصورة
            og_image = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
            if og_image and og_image.get("content"):
                details["image"] = og_image["content"]
                
            # 2. جلب العنوان
            og_title = soup.find("meta", property="og:title") or soup.find("title")
            if og_title:
                details["title"] = og_title.get("content") or og_title.text

            # 3. جلب السعر تلقائياً
            og_price = soup.find("meta", property="og:price:amount") or soup.find("meta", attrs={"name": "twitter:data1"})
            if og_price and og_price.get("content"):
                p_match = re.search(r'(\d+(\.\d+)?)', og_price["content"])
                if p_match:
                    details["price"] = float(p_match.group(1))

            if not details["price"]:
                json_scripts = soup.find_all('script', type='application/ld+json')
                for script in json_scripts:
                    if script.string:
                        try:
                            data = json.loads(script.string)
                            if isinstance(data, list):
                                data = data[0]
                            if isinstance(data, dict) and 'offers' in data:
                                offers = data['offers']
                                if isinstance(offers, list):
                                    offers = offers[0]
                                if 'price' in offers:
                                    details["price"] = float(offers['price'])
                                    break
                        except Exception:
                            continue
    except Exception:
        pass
    return details

# --- واجهة المستخدم ---
product_url = st.text_input("رابط المنتج", placeholder="https://www.shein.com/...")

scraped_image = None
scraped_title = None
auto_price = 0.0

if product_url:
    with st.spinner("جاري جلب تفاصيل المنتج والسعر تلقائياً..."):
        fetched = fetch_product_details(product_url)
        scraped_image = fetched.get("image")
        scraped_title = fetched.get("title")
        if fetched.get("price"):
            auto_price = float(fetched.get("price"))
        
    if scraped_image:
        st.image(scraped_image, caption=scraped_title or "صورة المنتج", use_column_width=True)
    elif scraped_title:
        st.info(f"المنتج: {scraped_title}")

with st.form("calc_form"):
    city = st.selectbox("اختر مدينة التوصيل", ["حضرموت", "عدن"])
    price_sar = st.number_input(
        "سعر المنتج بالريال السعودي (SAR)", 
        min_value=0.0, 
        value=auto_price, 
        step=1.0, 
        format="%.2f",
        help="يتم تعبئة السعر تلقائياً عند قراءة الرابط، ويمكنك تعديله يدوياً."
    )
    submitted = st.form_submit_button("احسب التكلفة")

if submitted:
    if price_sar <= 0:
        st.error("يرجى إدخال/التأكد من سعر المنتج.")
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
        
        # رسالة ضمان الشحنة
        st.warning("🛡️ **ضمان كافي أونلاين:** إذا لم تصلك شحنتك لأي سبب، نضمن لك استرجاع أموالك بالكامل.")
        
        # تجهيز رابط الواتساب
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
