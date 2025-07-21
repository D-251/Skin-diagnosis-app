import openai
import streamlit as st
# إعداد واجهة Streamlit
st.set_page_config(page_title="تشخيص البشرة", layout="centered")
st.title("🧴 مساعد تشخيص مشاكل البشرة")

# مدخلات المستخدم
gender = st.selectbox("👤 أنت:", ["أنثى", "ذكر"])
age = st.text_input("🎂 عمرك:")
symptoms = st.text_area("💬 اكتبي الأعراض اللي حاسة بيها في بشرتك:")

# عند الضغط على الزر
if st.button("🔍 شخّص الحالة"):
    with st.spinner("⏳ جاري تحليل الحالة..."):
        client = openai.OpenAI(
            api_key="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",
            base_url="https://openrouter.ai/api/v1",
        )

        message = f"""
        أنا {gender}، عمري {age} سنة.
        أعاني من الأعراض التالية: {symptoms}.

        📌 شخص الحالة كطبيب أمراض جلدية محترف، وقدم التالي:
        1- التشخيص المبدئي.
        2- اسم منتج محلي (اسم تجاري معروف في مصر) لعلاج الحالة + السعر + صورة المنتج (رابط إن أمكن).
        3- اسم منتج غالي أو عالمي معروف + السعر + صورة.
        4- لو المنتجات غير متوفرة، قدّم بدائل حقيقية بالأسماء التجارية.
        """

        chat_completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": "أنت طبيب أمراض جلدية محترف. قدم اقتراحات واضحة بناءً على السوق المصري."},
                {"role": "user", "content": message}
            ]
        )

        response_text = chat_completion.choices[0].message.content
        st.markdown("### 🧴 التشخيص والاقتراح:")
        st.markdown(response_text)

        # عرض الصور إن وُجدت
        product_images = {
            "بان أوكسيل": "https://i.imgur.com/LsGx4uc.jpg",
            "بنزاك": "https://i.imgur.com/VYx0clM.jpg",
            "ديفرين": "https://i.imgur.com/4tz6vPP.jpg",
            "ريتين-أ": "https://i.imgur.com/iT3eULe.jpg",
            "أكني فري": "https://i.imgur.com/9U8Vxjc.jpg",
            "إيزيس تين ديرم": "https://i.imgur.com/dRkgurZ.jpg"
        }

        st.markdown("### 📸 صور المنتجات المقترحة:")
        for name, url in product_images.items():
            if name.lower() in response_text.lower():
                st.image(url, caption=name, width=150)

# 💊 المتابعة بعد العلاج
st.markdown("---")
st.markdown("### 🔁 هل استخدمت العلاج؟")
follow_up = st.text_area("📋 اكتب إذا حصل تحسن أو ظهرت أعراض جديدة:")

if st.button("📤 أرسل للمتابعة"):
    with st.spinner("⏳ جاري تعديل خطة العلاج بناءً على المتابعة..."):
        followup_msg = f"""
مريض استخدم العلاج، وكتب التالي:
"{follow_up}"

⏳ عدّل خطة العلاج بناءً على ذلك.
"""
        followup_completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت طبيب تتابع الحالة بناءً على التطور."},
                {"role": "user", "content": followup_msg}
            ]
        )
        st.markdown("### 🔁 خطة العلاج بعد المتابعة:")
        st.markdown(followup_completion.choices[0].message.content)
