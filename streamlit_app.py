import streamlit as st
import urllib.parse

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(
    page_title="كافي أونلاين | التسوق الشامل",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصحيح تنسيق CSS لإظهار أسماء الأقسام بوضوح
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
        padding: 2.2rem 1rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-weight: 900;
        font-size: 2.2rem;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }
    
    .main-header p {
        color: #9ca3af;
        font-size: 1.05rem;
    }

    /* إصلاح ألوان أزرار الأقسام والخيارات */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        justify-content: center !important;
        margin-bottom: 1rem !important;
    }

    div[role="radiogroup"] > label {
        background-color: #ffffff !important;
        border: 1.5px solid #d1d5db !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
    }

    /* تحديد لون النص بشكل صريح ليظهر باللون الأسود/الداكن */
    div[role="radiogroup"] label p, 
    div[role="radiogroup"] label span {
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* التنسيق عند تحديد القسم */
    div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] p,
    div[role="radiogroup"] > label[data-checked="true"] span {
        color: #ffffff !important;
    }
    
    .product-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .product-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #111827;
        margin: 0.8rem 0;
        line-height: 1.4;
        height: 2.8em;
        overflow: hidden;
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
PHONE_NUMBER = "967770000000"
SAR_TO_YER = 425.0

# --- 3. قاعدة البيانات ---
if 'catalog' not in st.session_state:
    st.session_state.catalog = [
        # --- مستلزمات نسائية ---
        {
            "id": 1,
            "title": "طقم مجوهرات نسائية أنيق مكون من 4 قطع - قلادة فراشة، أقراط وحلقة ذهبية وردية",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 10.0,
            "image": "https://i.ibb.co/0jKxGpgM/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "طقم مجوهرات نسائية فراشة أقراط خاتم قلادة"
        },
        {
            "id": 2,
            "title": "طقم مجوهرات نسائية بتصميم زهرة المزالعة الخماسية (5 قطع)",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 11.0,
            "image": "https://i.ibb.co/qF10BHpn/image.jpg",
            "options_color": ["ذهبي", "فضي", "أسود"],
            "options_size": [],
            "tags": "طقم مجوهرات زهرة خماسية سوار أقراط خاتم"
        },
        {
            "id": 3,
            "title": "مجوهرات رجعية، وشم مفرغ، خيط صيد منسوج (3 قطع)",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 8.0,
            "image": "https://i.ibb.co/YBd8zGdG/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "مجوهرات وشم مفرغ خيط صيد قلادة مرنة سوار خاتم"
        },
        {
            "id": 4,
            "title": "4 أساور لؤلؤة ديزي - بلاستيك ورقيق زينك لطيفة (علامة 17 MILE)",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 8.0,
            "image": "https://i.ibb.co/qMFF4TTM/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "أساور لؤلؤ ديزي 17 mile إكسسوارات نسائية"
        },
        {
            "id": 5,
            "title": "قلادة حب جديدة بتصميم أوروبي وأمريكي متعددة الاستخدامات وسهلة",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 8.0,
            "image": "https://i.ibb.co/pjTqTqC8/image.jpg",
            "options_color": ["فضي", "ذهبي"],
            "options_size": [],
            "tags": "قلادة حب سلسلة مجوهرات فضي ذهبي"
        },
        {
            "id": 6,
            "title": "سوار سلسلة يد نسائي مودرن غربي عصري سهل المزج - كهدية",
            "main_category": "مستلزمات نسائية",
            "sub_category": "إكسسوارات",
            "price_sar": 8.0,
            "image": "https://i.ibb.co/SXQNB23L/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "سوار سلسلة يد مجوهرات هدايا نسائية"
        },

        # --- مستلزمات رجالية ---
        {
            "id": 7,
            "title": "تيشيرت رجالي أنيق بتصميم بسيط - ملون صلب مريح ومتين",
            "main_category": "مستلزمات رجالية",
            "sub_category": "ملابس",
            "price_sar": 17.0,
            "image": "https://i.ibb.co/3yBWgjJR/image.jpg",
            "options_color": ["أبيض"],
            "options_size": ["S", "L", "XL", "XXL"],
            "tags": "تيشيرت رجالي ملابس صيفي"
        },
        {
            "id": 8,
            "title": "تي شيرت ثلاثي الأبعاد للكبار بأكمام قصيرة مطبوع بنقشة - توب صيفي رياضي عصري",
            "main_category": "مستلزمات رجالية",
            "sub_category": "ملابس",
            "price_sar": 18.0,
            "image": "https://i.ibb.co/TMQ4DjfJ/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "تيشيرت 3D رياضي عصري أكمام قصيرة"
        },
        {
            "id": 9,
            "title": "تي شيرت رجالي عصري كاجوال - 100% ألياف، ياقة دائرية وقماش ناعم",
            "main_category": "مستلزمات رجالية",
            "sub_category": "ملابس",
            "price_sar": 20.0,
            "image": "https://i.ibb.co/RTCXncDC/image.jpg",
            "options_color": ["تدرج أسود برتقالي", "تدرج أزرق برتقالي", "تدرج كحلي أزرق"],
            "options_size": ["S", "M", "L", "XL", "XXL"],
            "tags": "تيشيرت كاجوال تدرج ألوان"
        },
        {
            "id": 10,
            "title": "قميص رجالي جديد بأكمام قصيرة وطوق (7 ألوان) - مريح وخفيف",
            "main_category": "مستلزمات رجالية",
            "sub_category": "ملابس",
            "price_sar": 21.0,
            "image": "https://i.ibb.co/NgzPbQR5/image.jpg",
            "options_color": ["7 ألوان متناسقة"],
            "options_size": ["XXL"],
            "tags": "قميص رجالي كم قصير طوق"
        },
        {
            "id": 11,
            "title": "بنطلون عمل رجالي عصري بجيوب متعددة - طويل مستقيم فضفاض",
            "main_category": "مستلزمات رجالية",
            "sub_category": "بناطيل",
            "price_sar": 34.0,
            "image": "https://i.ibb.co/8DDzzZw7/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "بنطلون عمل جيوب متعددة رجالي"
        },
        {
            "id": 12,
            "title": "بنطلون رجالي كاجوال برباط سحب - سريع الجفاف وذات التهوية",
            "main_category": "مستلزمات رجالية",
            "sub_category": "بناطيل",
            "price_sar": 24.0,
            "image": "https://i.ibb.co/JRtSCk25/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "بنطلون رباط سريع الجفاف رياضي"
        },
        {
            "id": 13,
            "title": "قميص رجالي صيفي بأكمام قصيرة بتصميم مريح ومكتوب للرحلات والعطلات",
            "main_category": "مستلزمات رجالية",
            "sub_category": "ملابس",
            "price_sar": 33.0,
            "image": "https://i.ibb.co/m5G66zMY/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "قميص صيفي رحلات عطلات"
        },
        {
            "id": 14,
            "title": "بنطلون رجالي فضفاض للعمل في الهواء الطلق والرياضة",
            "main_category": "مستلزمات رجالية",
            "sub_category": "بناطيل",
            "price_sar": 28.0,
            "image": "https://i.ibb.co/CqYS5C2/image.jpg",
            "options_color": [],
            "options_size": [],
            "tags": "بنطلون فضفاض عمل رياضة"
        },
        {
            "id": 15,
            "title": "حقيبة ظهر مخصصة للدراجات النارية مزودة بقفل حماية ضد السرقة (حقيبة كروس)",
            "main_category": "مستلزمات رجالية",
            "sub_category": "حقائب",
            "price_sar": 25.0,
            "image": "https://i.ibb.co/spvFyHTR/image.jpg",
            "options_color": [],
            "options_size": ["كبير", "صغير"],
            "tags": "حقيبة ظهر كروس دراجات نارية ضد السرقة"
        }
    ]

# --- 4. واجهة المستخدم ---

st.markdown("""
<div class="main-header">
    <h1>🛍️ كافي أونلاين</h1>
    <p>استكشف أحدث الموضة، المستلزمات والأجهزة المختارة بعناية</p>
</div>
""", unsafe_allow_html=True)

# البحث
search_query = st.text_input("🔍 ماذا تريد أن تطلب اليوم؟", placeholder="اكتب اسم المنتج أو نوعه (مثال: قميص، بنطلون، حقيبة، سوار...)")

# قائمة الأقسام الرئيسية
main_categories = ["الكل 🔥", "مستلزمات رجالية", "مستلزمات نسائية", "مستلزمات أطفال", "إلكترونيات", "أدوات منزلية"]
selected_main = st.radio("اختر القسم الرئيسي:", main_categories, horizontal=True, key="main_cat")

# الفلترة الفرعية
selected_sub = "الكل"
if selected_main in ["مستلزمات رجالية", "مستلزمات نسائية"]:
    sub_categories = ["الكل", "ملابس", "بناطيل", "حقائب", "إكسسوارات", "أحذية"]
    st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 10px; margin-bottom: 5px; color: #374151;'>التصنيف الفرعي:</p>", unsafe_allow_html=True)
    selected_sub = st.radio("اختر التصنيف الفرعي:", sub_categories, horizontal=True, key="sub_cat")

# تطبيق الفلترة
filtered_products = st.session_state.catalog

if selected_main != "الكل 🔥":
    filtered_products = [p for p in filtered_products if p["main_category"] == selected_main]

if selected_sub != "الكل":
    filtered_products = [p for p in filtered_products if p.get("sub_category") == selected_sub]

if search_query:
    filtered_products = [
        p for p in filtered_products 
        if search_query.lower() in p["title"].lower() or search_query.lower() in p["tags"].lower()
    ]

st.markdown("<br>", unsafe_allow_html=True)

# عرض المنتجات
if not filtered_products:
    st.info("لم نتمكن من العثور على منتجات تطابق اختيارك في هذا القسم حالياً.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtered_products):
        with cols[idx % 3]:
            price_yer = prod['price_sar'] * SAR_TO_YER
            
            selected_color = ""
            if prod.get("options_color"):
                selected_color = st.selectbox(f"اللون ({prod['title'][:12]}...):", prod["options_color"], key=f"col_{prod['id']}")
            
            selected_size = ""
            if prod.get("options_size"):
                selected_size = st.selectbox(f"المقاس ({prod['title'][:12]}...):", prod["options_size"], key=f"siz_{prod['id']}")
            
            color_text = f"\n- *اللون المختار:* {selected_color}" if selected_color else ""
            size_text = f"\n- *المقاس المختار:* {selected_size}" if selected_size else ""
            
            message = f"مرحباً بكافي أونلاين 👋\nأرغب في طلب المنتج التالي:\n- *المنتج:* {prod['title']}{color_text}{size_text}\n- *السعر:* {prod['price_sar']} ر.س ({price_yer:,.0f} ر.ي)\n- *الرابط:* {prod['image']}"
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{PHONE_NUMBER}?text={encoded_message}"
            
            share_text = f"شاهد هذا المنتج المميز من كافي أونلاين: {prod['title']} بسعر {prod['price_sar']} ر.س"
            encoded_share = urllib.parse.quote(share_text)
            share_url = f"https://api.whatsapp.com/send?text={encoded_share}"

            st.markdown(f"""
            <div class="product-card">
                <img src="{prod['image']}" style="width: 100%; height: 220px; object-fit: cover; border-radius: 12px;">
                <div class="product-title">{prod['title']}</div>
                <div class="price-tag-sar">{prod['price_sar']} <small>ر.س</small></div>
                <div class="price-tag-yer">يعادل تقريباً: {price_yer:,.0f} ر.ي</div>
                <a href="{share_url}" target="_blank" class="share-btn">📲 مشاركة المنتج</a>
                <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">💬 اطلب عبر الواتساب</a>
            </div>
            """, unsafe_allow_html=True)

# الفوتر
st.markdown("""
<div class="footer">
    <p>© 2026 كافي أونلاين - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
