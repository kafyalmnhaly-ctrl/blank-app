import streamlit as st
import urllib.parse

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="كافي أونلاين | التسوق الشامل",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. التنسيق البصري المتكيف للنهار والليل ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(180deg, #f3f4f6 0%, #e5e7eb 100%);
    }

    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
    }
    
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%);
        color: white;
        padding: 2.5rem 1rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.3);
    }
    
    .main-header h1 {
        font-weight: 900;
        font-size: 2.4rem;
        color: #ffffff !important;
        margin-bottom: 0.4rem;
    }
    
    .main-header p {
        color: #e0e7ff;
        font-size: 1.1rem;
        font-weight: 600;
    }

    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
        justify-content: center !important;
        margin-bottom: 1.2rem !important;
    }

    div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(8px);
        border: 2px solid #e5e7eb !important;
        border-radius: 16px !important;
        padding: 10px 20px !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    div[role="radiogroup"] label p, 
    div[role="radiogroup"] label span {
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border-color: #2563eb !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] p,
    div[role="radiogroup"] > label[data-checked="true"] span {
        color: #ffffff !important;
    }
    
    .product-card-thumb {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.2rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    .product-title-thumb {
        font-size: 1rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.8rem 0 0.4rem 0;
        line-height: 1.4;
        height: 2.8em;
        overflow: hidden;
    }
    
    .price-tag-sar {
        font-size: 1.35rem;
        font-weight: 900;
        color: #059669;
    }
    
    .price-tag-yer {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.6rem;
    }
    
    .whatsapp-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #25d366 0%, #16a34a 100%);
        color: white !important;
        text-align: center;
        padding: 0.75rem;
        border-radius: 12px;
        font-weight: 700;
        text-decoration: none;
        margin-top: 0.8rem;
    }

    .footer {
        text-align: center;
        padding: 2.5rem;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        margin-top: 3.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. إعدادات المتجر العامة ---
PHONE_NUMBER = "967770000000"
SAR_TO_YER = 425.0

# --- 4. قاعدة البيانات (مع التحديث التلقائي) ---
raw_catalog = [
    {
        "id": 1,
        "title": "طقم مجوهرات نسائية أنيق مكون من 4 قطع - قلادة فراشة، أقراط وحلقة ذهبية وردية",
        "main_category": "مستلزمات نسائية",
        "sub_category": "إكسسوارات",
        "price_sar": 10.0,
        "images": ["https://i.ibb.co/0jKxGpgM/image.jpg"],
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
        "images": ["https://i.ibb.co/qF10BHpn/image.jpg"],
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
        "images": ["https://i.ibb.co/YBd8zGdG/image.jpg"],
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
        "images": ["https://i.ibb.co/qMFF4TTM/image.jpg"],
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
        "images": ["https://i.ibb.co/pjTqTqC8/image.jpg"],
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
        "images": ["https://i.ibb.co/SXQNB23L/image.jpg"],
        "options_color": [],
        "options_size": [],
        "tags": "سوار سلسلة يد مجوهرات هدايا نسائية"
    },
    {
        "id": 7,
        "title": "تيشيرت رجالي أنيق بتصميم بسيط - ملون صلب مريح ومتين",
        "main_category": "مستلزمات رجالية",
        "sub_category": "ملابس",
        "price_sar": 17.0,
        "images": [
            "https://i.ibb.co/3yBWgjJR/image.jpg",
            "https://i.ibb.co/C5NNWbM2/image.jpg",
            "https://i.ibb.co/G3MS2TPL/image.jpg",
            "https://i.ibb.co/Y4wMtBZp/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/TMQ4DjfJ/image.jpg",
            "https://i.ibb.co/WNfD2rp7/image.jpg",
            "https://i.ibb.co/Kcwnnz6t/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/RTCXncDC/image.jpg",
            "https://i.ibb.co/qLKFKs5J/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/NgzPbQR5/image.jpg",
            "https://i.ibb.co/6ch5pj2L/image.jpg",
            "https://i.ibb.co/1Jm5Fd2Q/image.jpg",
            "https://i.ibb.co/wZcKHx4t/image.jpg",
            "https://i.ibb.co/qLztSyNX/image.jpg",
            "https://i.ibb.co/G4hq5rZv/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/8DDzzZw7/image.jpg",
            "https://i.ibb.co/Xr0CmSm1/image.jpg",
            "https://i.ibb.co/HDqRCjGb/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/JRtSCk25/image.jpg",
            "https://i.ibb.co/Xx1bj0Cr/image.jpg",
            "https://i.ibb.co/1fNN5w8J/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/m5G66zMY/image.jpg",
            "https://i.ibb.co/svmPWBVM/image.jpg",
            "https://i.ibb.co/hF1bSRct/image.jpg",
            "https://i.ibb.co/RpTRw9qy/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/CqYS5C2/image.jpg",
            "https://i.ibb.co/LXP725ZT/image.jpg",
            "https://i.ibb.co/yKFqg9B/image.jpg"
        ],
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
        "images": [
            "https://i.ibb.co/spvFyHTR/image.jpg",
            "https://i.ibb.co/F4DPsMQW/image.jpg"
        ],
        "options_color": [],
        "options_size": ["كبير", "صغير"],
        "tags": "حقيبة ظهر كروس دراجات نارية ضد السرقة"
    }
]

# تحديث Session State لضمان وجود حقل images لجميع المنتجات
st.session_state.catalog = raw_catalog

# --- 5. نافذة التفاصيل والصور ---
@st.dialog("عرض تفاصيل المنتج 🛍️")
def show_product_details(prod):
    price_yer = prod['price_sar'] * SAR_TO_YER
    st.subheader(prod['title'])
    
    prod_images = prod.get('images', [prod.get('image', '')])
    
    st.markdown("##### 📸 صور المنتج:")
    if len(prod_images) == 1:
        st.image(prod_images[0], use_container_width=True)
    else:
        img_cols = st.columns(min(len(prod_images), 3))
        for idx, img in enumerate(prod_images):
            with img_cols[idx % 3]:
                st.image(img, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    selected_color = ""
    selected_size = ""
    
    with col1:
        if prod.get("options_color"):
            selected_color = st.selectbox("اختر اللون:", prod["options_color"], key=f"dlg_col_{prod['id']}")
    with col2:
        if prod.get("options_size"):
            selected_size = st.selectbox("اختر المقاس:", prod["options_size"], key=f"dlg_siz_{prod['id']}")
            
    st.markdown(f"**السعر:** <span class='price-tag-sar'>{prod['price_sar']} ر.س</span> (<small>~ {price_yer:,.0f} ر.ي</small>)", unsafe_allow_html=True)
    
    color_text = f"\n- *اللون المختار:* {selected_color}" if selected_color else ""
    size_text = f"\n- *المقاس المختار:* {selected_size}" if selected_size else ""
    
    first_img = prod_images[0] if prod_images else ""
    message = f"مرحباً بكافي أونلاين 👋\nأرغب في طلب المنتج التالي:\n- *المنتج:* {prod['title']}{color_text}{size_text}\n- *السعر:* {prod['price_sar']} ر.س ({price_yer:,.0f} ر.ي)\n- *الرابط:* {first_img}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{PHONE_NUMBER}?text={encoded_message}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">💬 طلب المنتج عبر الواتساب</a>', unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية والتصفح ---

st.markdown("""
<div class="main-header">
    <h1>✨ كافي أونلاين ✨</h1>
    <p>وجهتك الأولى لتسوق أفضل المستلزمات العصرية والمنتجات المختارة</p>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input("🔍 البحث في المتجر:", placeholder="اكتب اسم المنتج، النوع، أو الكلمة المفتاحية...")

main_categories = ["الكل 🔥", "مستلزمات رجالية", "مستلزمات نسائية", "مستلزمات أطفال", "إلكترونيات", "أدوات منزلية"]
selected_main = st.radio("اختر القسم الرئيسي:", main_categories, horizontal=True, key="main_cat")

selected_sub = "الكل"
if selected_main in ["مستلزمات رجالية", "مستلزمات نسائية"]:
    sub_categories = ["الكل", "ملابس", "بناطيل", "حقائب", "إكسسوارات", "أحذية"]
    st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 5px; color: #3b82f6;'>الفئة الفرعية:</p>", unsafe_allow_html=True)
    selected_sub = st.radio("اختر التصنيف الفرعي:", sub_categories, horizontal=True, key="sub_cat")

filtered_products = st.session_state.catalog

if selected_main != "الكل 🔥":
    filtered_products = [p for p in filtered_products if p.get("main_category") == selected_main]

if selected_sub != "الكل":
    filtered_products = [p for p in filtered_products if p.get("sub_category") == selected_sub]

if search_query:
    filtered_products = [
        p for p in filtered_products 
        if search_query.lower() in p.get("title", "").lower() or search_query.lower() in p.get("tags", "").lower()
    ]

st.markdown("<br>", unsafe_allow_html=True)

# عرض المنتجات
if not filtered_products:
    st.info("لم نتمكن من العثور على منتجات تطابق اختيارك في هذا القسم حالياً.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtered_products):
        with cols[idx % 3]:
            price_yer = prod.get('price_sar', 0) * SAR_TO_YER
            
            # جلب الصورة المصغرة بأمان لمنع أي KeyError
            prod_images = prod.get('images', [prod.get('image', '')])
            thumb_img = prod_images[0] if prod_images else ''
            
            st.markdown(f"""
            <div class="product-card-thumb">
                <img src="{thumb_img}" style="width: 100%; height: 170px; object-fit: cover; border-radius: 14px;">
                <div class="product-title-thumb">{prod.get('title', '')}</div>
                <div class="price-tag-sar">{prod.get('price_sar', 0)} <small>ر.س</small></div>
                <div class="price-tag-yer">يعادل تقريباً: {price_yer:,.0f} ر.ي</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 عرض الصور والتفاصيل", key=f"btn_details_{prod.get('id', idx)}", use_container_width=True):
                show_product_details(prod)

# الفوتر
st.markdown("""
<div class="footer">
    <p>© 2026 كافي أونلاين - تجربة تسوق فريدة ومتميزة</p>
</div>
""", unsafe_allow_html=True)
