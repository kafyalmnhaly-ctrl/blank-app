import streamlit as st
import urllib.parse

# --- 1. إعدادات الصفحة والتصميم الجذاب ---
st.set_page_config(
    page_title="كافي أونلاين | التسوق الشامل",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تنسيق CSS مخصص للواجهة
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 2.6rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    .share-container {
        text-align: center;
        margin-bottom: 25px;
    }
    .share-btn {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        text-decoration: none;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
        transition: transform 0.2s;
    }
    .share-btn:hover {
        transform: scale(1.05);
    }
    .search-box {
        background-color: #1f1f1f;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .price-tag {
        color: #4CAF50;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 5px 0;
    }
    .tag-badge {
        background-color: #4A1515;
        color: #FF4B4B;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. الثوابت وحاسبة العملة ---
EXCHANGE_RATE = 445.0  # سعر الصرف بالريال اليمني مقابل الريال السعودي
WHATSAPP_NUMBER = "966580384981"  # رقم الواتساب الخاص بك
STORE_URL = "https://kafyalmnhaly-blank-app-streamlit-app-5s1203.streamlit.app"  # رابط متجرك

# نص رسالة مشاركة المتجر
SHARE_MSG = f"تسوق أونلاين بأفضل الأسعار وأحدث المنتجات من متجر *كافي أونلاين* 🛍️✨\n\nتصفح المنتجات واطلب فوراً عبر هذا الرابط:\n{STORE_URL}"
SHARE_WA_URL = f"https://wa.me/?text={urllib.parse.quote(SHARE_MSG)}"

# --- 3. قاعدة بيانات المنتجات ---
if 'catalog' not in st.session_state:
    st.session_state.catalog = [
        # ملابس نساء
        {"id": 1, "title": "فستان صيفي أنيق", "category": "ملابس نساء", "price_sar": 85.0, "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=500", "tags": "فستان نسائي ملابس صيفي نساء"},
        {"id": 2, "title": "عباية مودرن راقية", "category": "ملابس نساء", "price_sar": 150.0, "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500", "tags": "عباية نساء ملابس خروج"},
        
        # أحذية وحقائب
        {"id": 14, "title": "حذاء رياضي نسائي أنيق", "category": "أحذية وحقائب", "price_sar": 56.76, "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500", "tags": "حذاء شوز جزمه رياضي نسائي كاجوال 2026"},

        # ملابس رجال
        {"id": 3, "title": "قميص كاجوال رجالي", "category": "ملابس رجال", "price_sar": 65.0, "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500", "tags": "قميص رجالي ثوب بلوزة رجال"},
        {"id": 4, "title": "جاكيت شتوي أنيق", "category": "ملابس رجال", "price_sar": 130.0, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500", "tags": "جاكيت كوت شتاء رجال"},
        
        # ملابس أطفال
        {"id": 5, "title": "طقم أطفال قطني مريح", "category": "ملابس أطفال", "price_sar": 45.0, "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500", "tags": "طفل أطفال طقم ملابس ولادي بناتي"},
        {"id": 6, "title": "فستان بناتي صغير", "category": "ملابس أطفال", "price_sar": 50.0, "image": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=500", "tags": "فستان أطفال بناتي زهور"},
        
        # ساعات
        {"id": 7, "title": "ساعة يد كلاسيك رجالية", "category": "ساعات", "price_sar": 120.0, "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500", "tags": "ساعة ساعات جلد رجالي"},
        {"id": 8, "title": "ساعة ذكية مقاومة للماء", "category": "ساعات", "price_sar": 110.0, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", "tags": "ساعة ذكية ساعات smart watch"},
        
        # إكسسوارات
        {"id": 9, "title": "سوار ذهبي أنيق", "category": "إكسسوارات", "price_sar": 40.0, "image": "https://images.unsplash.com/photo-1611591475281-b1c9ad53741c?w=500", "tags": "سوار إسوارة مجوهرات إكسسوارات نسائي"},
        {"id": 10, "title": "نظارة شمسية كلاسيك", "category": "إكسسوارات", "price_sar": 55.0, "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500", "tags": "نظارة شمس إكسسوارات رجالي نسائي"},
        
        # عناية وتجميل
        {"id": 11, "title": "طقم عناية بالبشرة متكامل", "category": "عناية", "price_sar": 95.0, "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500", "tags": "عناية بشرة كريم غسول تجميل"},
        {"id": 12, "title": "عطر رجالي فخم", "category": "عناية", "price_sar": 140.0, "image": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=500", "tags": "عطر عناية بخور عطور"},
        
        # إلكترونيات
        {"id": 13, "title": "سماعات بلوتوث لاسلكية", "category": "إلكترونيات", "price_sar": 75.0, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "tags": "سماعة بلوتوث إلكترونيات ايربودز"},
    ]

# --- 4. واجهة الموقع ---
st.markdown("<h1 class='main-title'>كافي أونلاين 🛍️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>ابحث عن أي غرض أو اختر من الأقسام التالية</p>", unsafe_allow_html=True)

# زر مشاركة الموقع عبر الواتساب في الأعلى
st.markdown(f"""
    <div class='share-container'>
        <a href='{SHARE_WA_URL}' target='_blank' class='share-btn'>
            📲 شارك المتجر مع الأصدقاء على الواتساب
        </a>
    </div>
""", unsafe_allow_html=True)

# شريط البحث الرئيسي
st.markdown("<div class='search-box'>", unsafe_allow_html=True)
search_query = st.text_input("🔍 ماذا تريد أن تطلب اليوم؟", placeholder="اكتب اسم الغرض (مثال: فستان، حذاء، ساعة، قميص...)")
st.markdown("</div>", unsafe_allow_html=True)

# قائمة الأقسام الموسعة
categories = ["الكل", "🔥 العروض", "أحذية وحقائب", "ملابس نساء", "ملابس رجال", "ملابس أطفال", "ساعات", "إكسسوارات", "عناية", "إلكترونيات"]
selected_category = st.radio("تصفح القسم:", categories, horizontal=True)

# --- 5. فلترة البحث والمنتجات المشابهة ---
matched_products = []
similar_products = []

if search_query.strip():
    query = search_query.strip().lower()
    for item in st.session_state.catalog:
        if query in item["title"].lower() or query in item["tags"].lower() or query in item["category"].lower():
            matched_products.append(item)
    
    if matched_products:
        matched_cats = {p["category"] for p in matched_products}
        matched_ids = {p["id"] for p in matched_products}
        similar_products = [
            p for p in st.session_state.catalog 
            if p["category"] in matched_cats and p["id"] not in matched_ids
        ]
else:
    if selected_category == "🔥 العروض":
        matched_products = [p for p in st.session_state.catalog if p["price_sar"] <= 75.0]
    elif selected_category != "الكل":
        matched_products = [p for p in st.session_state.catalog if p["category"] == selected_category]
    else:
        matched_products = st.session_state.catalog

# --- 6. دالة عرض الكروت ---
def render_product_card(prod, badge_text=None):
    tot_sar = prod["price_sar"]
    tot_yer = tot_sar * EXCHANGE_RATE
    
    st.markdown("<div class='product-card'>", unsafe_allow_html=True)
    if badge_text:
        st.markdown(f"<span class='tag-badge'>{badge_text}</span>", unsafe_allow_html=True)
    
    st.image(prod["image"], use_container_width=True)
    st.subheader(prod["title"])
    st.markdown(f"<p class='price-tag'>{tot_yer:,.0f} ر.ي</p>", unsafe_allow_html=True)
    st.caption(f"السعر: {prod['price_sar']} ر.س")
    
    msg = f"السلام عليكم، أرغب بطلب المنتج التالي عبر كافي أونلاين:\n📦 المنتج: {prod['title']}\n📂 القسم: {prod['category']}\n💰 السعر: {tot_yer:,.0f} ريال يمني ({prod['price_sar']} ر.س)"
    wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; background-color:#25D366; color:white; padding:8px; border-radius:6px; font-weight:bold; text-decoration:none; font-size:0.9rem;">اطلبه الآن 📲</a>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. عرض النتائج ---
st.write("---")

if search_query.strip():
    if matched_products:
        st.success(f"🎯 وجدت لك **{len(matched_products)}** منتج يطابق بحثك:")
        cols = st.columns(3)
        for idx, prod in enumerate(matched_products):
            with cols[idx % 3]:
                render_product_card(prod, "مطابق للبحث 🎯")
        
        if similar_products:
            st.write("---")
            st.subheader("💡 أغراض مشابهة قد تعجبك:")
            sim_cols = st.columns(3)
            for idx, prod in enumerate(similar_products):
                with sim_cols[idx % 3]:
                    render_product_card(prod, "مقترح لك ⭐")
    else:
        st.warning(f"لم أجد منتجاً باسم '{search_query}'. يمكنك طلب هذا الغرض تحديداً عبر الواتساب:")
        custom_msg = f"السلام عليكم، أبحث عن غرض باسم: ({search_query}) هل هو متوفر لديكم؟"
        custom_wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(custom_msg)}"
        st.markdown(f'<a href="{custom_wa_url}" target="_blank" style="display:inline-block; background-color:#25D366; color:white; padding:10px 20px; border-radius:6px; font-weight:bold; text-decoration:none;">📲 اسألنا عن هذا الغرض عبر الواتساب</a>', unsafe_allow_html=True)

else:
    cols = st.columns(3)
    for idx, prod in enumerate(matched_products):
        with cols[idx % 3]:
            render_product_card(prod)

# --- 8. الفوتر وزر المشاركة السفلية ---
st.write("---")
st.info("📍 **مناطق التوصيل:** حضرموت - عدن فقط | ضمان استرجاع 100%")

st.markdown(f"""
    <div style='text-align: center; margin-top: 15px;'>
        <p style='color: #888;'>أعجبك المتجر؟ شاركه مع من تحب 🔗</p>
        <a href='{SHARE_WA_URL}' target='_blank' class='share-btn'>
            📲 مشاركة رابط المتجر عبر الواتساب
        </a>
    </div>
""", unsafe_allow_html=True)
