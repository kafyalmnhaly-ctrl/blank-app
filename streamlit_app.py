from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import quote, urlparse

import streamlit as st


SERVICE_FEE_RATE = 0.05
ESTIMATED_SHIPPING_USD = 5.0
USD_TO_YER = 1680


@dataclass(frozen=True)
class Quote:
    product_url: str
    product_price_usd: float
    service_fee_usd: float
    shipping_usd: float
    total_usd: float
    total_yer: int


# Replace the account placeholders with the confirmed merchant details.
BANK_DETAILS = (
    {
        "name": "مصرف الكريمي",
        "account_name": "يُضاف اسم صاحب الحساب",
        "account_number": "يُضاف رقم الحساب",
    },
    {
        "name": "بنك أمقي",
        "account_name": "يُضاف اسم صاحب الحساب",
        "account_number": "يُضاف رقم الحساب",
    },
)


def format_usd(value: float) -> str:
    return f"${value:,.2f}"


def format_yer(value: int) -> str:
    return f"{value:,} ريال"


def is_valid_product_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalize_phone_number(value: str) -> str:
    return re.sub(r"\D", "", value)


def build_whatsapp_url(phone_number: str, quote_data: Quote) -> str:
    message = (
        "مرحباً، أريد تأكيد طلب شراء:\n"
        f"رابط المنتج: {quote_data.product_url}\n"
        f"سعر المنتج: {format_usd(quote_data.product_price_usd)}\n"
        f"الإجمالي بالدولار: {format_usd(quote_data.total_usd)}\n"
        f"الإجمالي بالريال اليمني: {format_yer(quote_data.total_yer)}"
    )
    return f"https://wa.me/{phone_number}?text={quote(message)}"


def inject_rtl_styles() -> None:
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stSidebar"], [data-testid="stHeader"] {
            direction: rtl;
        }
        [data-testid="stAppViewContainer"] * {
            text-align: right;
        }
        [data-testid="stMetricValue"] {
            direction: ltr;
            text-align: right;
        }
        [data-testid="stMetricLabel"] {
            text-align: right;
        }
        .quote-header {
            border-right: 4px solid #d28b45;
            padding: 0.15rem 0.9rem 0.25rem 0;
            margin: 1rem 0 0.75rem;
        }
        .quote-header h2 {
            margin-bottom: 0.15rem;
        }
        .quote-header p {
            color: #69727d;
            margin: 0;
        }
        .bank-card {
            border: 1px solid rgba(49, 51, 63, 0.18);
            border-radius: 0.75rem;
            padding: 1rem 1.1rem;
            min-height: 150px;
            background: rgba(255, 255, 255, 0.55);
        }
        .bank-card h3 {
            margin: 0 0 0.8rem;
        }
        .bank-card p {
            margin: 0.35rem 0;
        }
        .bank-label {
            color: #69727d;
            font-size: 0.85rem;
        }
        .bank-value {
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_quote(quote_data: Quote) -> None:
    st.markdown(
        """
        <div class="quote-header">
            <h2>ملخص التكلفة</h2>
            <p>هذه هي التكلفة التقديرية للطلب قبل الدفع.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(3)
    with metric_columns[0]:
        st.metric("سعر المنتج", format_usd(quote_data.product_price_usd))
    with metric_columns[1]:
        st.metric("رسوم الخدمة (5%)", format_usd(quote_data.service_fee_usd))
    with metric_columns[2]:
        st.metric("الشحن التقديري", format_usd(quote_data.shipping_usd))

    st.success(
        f"الإجمالي التقديري: {format_usd(quote_data.total_usd)}  "
        f"يعادل تقريباً **{format_yer(quote_data.total_yer)}**"
    )
    st.caption(
        f"سعر التحويل المستخدم: 1 دولار = {USD_TO_YER:,} ريال يمني. "
        "قد يختلف المبلغ النهائي إذا تغيّر سعر الصرف أو الشحن الفعلي."
    )


def render_payment_details(quote_data: Quote) -> None:
    st.markdown(
        """
        <div class="quote-header">
            <h2>طريقة الدفع</h2>
            <p>حوّل المبلغ إلى أحد الحسابين، ثم أرسل صورة الإيصال للتأكيد.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    bank_columns = st.columns(2)
    for column, bank in zip(bank_columns, BANK_DETAILS):
        with column:
            st.markdown(
                f"""
                <div class="bank-card">
                    <h3>{bank["name"]}</h3>
                    <p><span class="bank-label">اسم الحساب:</span><br>
                    <span class="bank-value">{bank["account_name"]}</span></p>
                    <p><span class="bank-label">رقم الحساب:</span><br>
                    <span class="bank-value">{bank["account_number"]}</span></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "مهم: تأكد من اسم صاحب الحساب ورقم الحساب قبل التحويل. "
        "بيانات الحساب الظاهرة حالياً تحتاج إلى تحديث من إدارة المتجر."
    )

    st.markdown("#### تأكيد الدفع عبر واتساب")
    whatsapp_number = st.text_input(
        "رقم واتساب المتجر",
        placeholder="مثال: 9677XXXXXXX",
        help="اكتب الرقم مع مفتاح الدولة، مثل 967، بدون علامة +.",
    )
    normalized_number = normalize_phone_number(whatsapp_number)

    if normalized_number:
        st.link_button(
            "إرسال تفاصيل الطلب عبر واتساب",
            build_whatsapp_url(normalized_number, quote_data),
            use_container_width=True,
        )
    else:
        st.button(
            "إرسال تفاصيل الطلب عبر واتساب",
            disabled=True,
            use_container_width=True,
            help="أدخل رقم واتساب المتجر لتفعيل الزر.",
        )
        st.caption("أدخل رقم واتساب المتجر أولاً لتفعيل زر التأكيد.")


def main() -> None:
    st.set_page_config(
        page_title="سوق اليمن | حاسبة تكلفة الطلب",
        page_icon="س",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_rtl_styles()

    st.title("سوق اليمن")
    st.subheader("حاسبة تكلفة الطلب من الخارج")
    st.write(
        "أدخل رابط المنتج وسعره بالدولار لمعرفة التكلفة التقديرية "
        "بالريال اليمني قبل إتمام الدفع."
    )

    with st.form("quote_form"):
        product_url = st.text_input(
            "رابط المنتج",
            placeholder="https://example.com/product",
            help="أدخل الرابط الكامل للمنتج الذي تريد شراءه.",
        )
        product_price_usd = st.number_input(
            "سعر المنتج بالدولار الأمريكي",
            min_value=0.0,
            step=1.0,
            format="%.2f",
            help="اكتب سعر المنتج كما يظهر في الموقع.",
        )
        submitted = st.form_submit_button(
            "احسب التكلفة",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not product_url.strip():
            st.error("يرجى إدخال رابط المنتج.")
        elif not is_valid_product_url(product_url):
            st.error("يرجى إدخال رابط صحيح يبدأ بـ http:// أو https://.")
        elif product_price_usd <= 0:
            st.error("يرجى إدخال سعر أكبر من صفر.")
        else:
            service_fee = product_price_usd * SERVICE_FEE_RATE
            total_usd = (
                product_price_usd + service_fee + ESTIMATED_SHIPPING_USD
            )
            st.session_state.quote = Quote(
                product_url=product_url.strip(),
                product_price_usd=product_price_usd,
                service_fee_usd=service_fee,
                shipping_usd=ESTIMATED_SHIPPING_USD,
                total_usd=total_usd,
                total_yer=round(total_usd * USD_TO_YER),
            )

    quote_data = st.session_state.get("quote")
    if quote_data:
        render_quote(quote_data)
        render_payment_details(quote_data)

    st.divider()
    st.caption(
        f"رسوم الخدمة {SERVICE_FEE_RATE:.0%} • الشحن التقديري "
        f"{format_usd(ESTIMATED_SHIPPING_USD)} • سعر الصرف {USD_TO_YER:,}"
    )


if __name__ == "__main__":
    main()