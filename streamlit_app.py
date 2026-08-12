import streamlit as st
import urllib.parse

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(
    page_title="كافي أونلاين | التسوق الشامل",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تحسين الهوية البصرية وإصلاح ظهور الأقسام
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: white;
        padding: 2.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-weight: 900;
        font-size: 2.2rem;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #9ca3af;
        font-size: 1.1rem;
    }
    
    /* إصلاح نص خيارات الأقسام */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
    }
    
    .product-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    
    .product-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin: 0.8rem 0;
        line-height: 1.4;
    }
    
    .price-tag-sar {
        font-size: 1.3rem;
        font-weight: 900;
        color: #059669;
    }
    
    .price-tag-yer {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25d366;
        color: white !important;
        text-align: center;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 700;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.2);
    }

    .share-btn {
        display: block;
        width: 100%;
        background-color: #0088cc;
        color: white !important;
        text-align: center;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 700;
        text-decoration: none;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 136, 204, 0.2);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. إعدادات المتجر العامة ---
PHONE_NUMBER = "967770000000"  # ضع رقم الواتساب الخاص بك هنا
SAR_TO_YER = 425.0             # سعر الصرف

# --- 3. قاعدة بيانات المنتجات ---
if 'catalog' not in st.session_state:
    st.session_state.catalog = [
        {
            "id": 1, 
            "title": "2026 أحذية رياضية أرثوبيدية سميكة الأساس للنساء", 
            "category": "أحذية وحقائب", 
            "price_sar": 55.0, 
            "image": "https://i.ibb.co/SDMDv3MH/image.jpg", 
            "tags": "حذاء رياضي نسائي أرثوبيدي كاجوال نعل سميك أربطة مريح 2026"
        },
    ]

# --- 4. واجهة الموقع ---

# الهيدر الرئيسي
st.markdown("""
<div class="main-header">
    <h1>🛍️ كافي أونلاين</h1>
    <p>استكشف أحدث الموضة والأجهزة والمنتجات المختارة</p>
</div>
""", unsafe_allow_html=True)

# قسم البحث
search_query = st.text_input("🔍 ماذا تريد أن تطلب اليوم؟", placeholder="اكتب اسم المنتج (مثال: فستان، حذاء، ساعة، قميص...)")

# قائمة الأقسام بأسلوب القائمة المنسدلة الواضحة
categories = ["الكل 🔥", "ملابس نساء", "ملابس رجال", "ملابس أطفال", "أحذية وحقائب", "ساعات", "إكسسوارات", "عناية", "إلكترونيات"]
selected_category = st.selectbox("اختر قسم المتجر عرضاً:", categories)

# فلترة المنتجات
filtered_products = st.session_state.catalog

if selected_category != "الكل 🔥":
    filtered_products = [p for p in filtered_products if p["category"] == selected_category]

if search_query:
    filtered_products = [
        p for p in filtered_products 
        if search_query.lower() in p["title"].lower() or search_query.lower() in p["tags"].lower()
    ]

st.markdown("<br>", unsafe_allow_html=True)

# عرض المنتجات
if not filtered_products:
    st.info("لم نتمكن من العثور على منتجات تطابق بحثك في هذا القسم حالياً.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtered_products):
        with cols[idx % 3]:
            price_yer = prod['price_sar'] * SAR_TO_YER
            
            message = f"مرحباً بكافي أونلاين 👋\nأرغب في طلب المنتج التالي:\n- *المنتج:* {prod['title']}\n- *السعر:* {prod['price_sar']} ر.س ({price_yer:,.0f} ر.ي)\n- *الرابط:* {prod['image']}"
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{PHONE_NUMBER}?text={encoded_message}"
            
            share_text = f"شاهد هذا المنتج المميز من كافي أونلاين: {prod['title']} بسعر {prod['price_sar']} ر.س"
            encoded_share = urllib.parse.quote(share_text)
            share_url = f"https://api.whatsapp.com/send?text={encoded_share}"

            st.markdown(f"""
            <div class="product-card">
                <div>
                    <img src="{prod['image']}" style="width: 100%; height: 220px; object-fit: cover; border-radius: 12px;">
                    <div class="product-title">{prod['title']}</div>
                </div>
                <div>
                    <div class="price-tag-sar">{prod['price_sar']} <small>ر.س</small></div>
                    <div class="price-tag-yer">يعادل تقريباً: {price_yer:,.0f} ر.ي</div>
                    <a href="{share_url}" target="_blank" class="share-btn">📲 مشاركة المنتج</a>
                    <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">💬 اطلب عبر الواتساب</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# الفوتر
st.markdown("""
<div class="footer">
    <p>© 2026 كافي أونلاين - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
