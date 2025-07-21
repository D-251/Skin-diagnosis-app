import openai

client = openai.OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
)

gender = input("👤 أنت ذكر أم أنثى؟: ").strip().lower()
age = input("🎂 ما هو عمرك؟: ").strip()
symptoms = input("💬 اكتبي الأعراض اللي حاسة بيها في بشرتك: ").strip()

message = f"""
أنا {'ذكر' if gender == 'ذكر' else 'أنثى'}، عمري {age} سنة.
أعاني من الأعراض التالية: {symptoms}.

📌 شخص الحالة كطبيب أمراض جلدية محترف، وقدم التالي:

1- التشخيص المبدئي.
2- اسم منتج محلي (اسم تجاري معروف في مصر) لعلاج الحالة + السعر + صورة المنتج (رابط إن أمكن).
3- اسم منتج غالي أو عالمي معروف + السعر + صورة.
4- لو المنتجات غير متوفرة، قدّم بدائل حقيقية بالأسماء التجارية.


رجاءً لا تستخدم وصف عام فقط، اذكر أسماء المنتجات كما تُباع في السوق فعلًا.
"""

chat_completion = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    messages=[
{"role": "system", "content": """أنت طبيب أمراض جلدية محترف. هدفك:
- تشخيص الأعراض بشكل مبدئي.
- ترشيح منتج محلي مصري موثوق *بالاسم التجاري الحقيقي* وسعره.
- ترشيح منتج غالي أو عالمي *بالاسم التجاري* وسعره.
- في كل منتج، اذكر الاسم التجاري بوضوح مع صورة إن أمكن (رابط مباشر).
- قدّم بدائل بالأسماء التجارية أيضًا لو المنتج غير متوفر.
- في النهاية، قل إن كانت الحالة تستدعي زيارة طبيب أم لا.

اكتب الرد بلغة عربية سهلة ومنظمة.
"""},
        {"role": "user", "content": message}
    ]
)
product_images = {
    "بان أوكسيل": "https://i.imgur.com/LsGx4uc.jpg",
    "بنزاك": "https://i.imgur.com/VYx0clM.jpg",
    "ديفرين": "https://i.imgur.com/4tz6vPP.jpg",
    "ريتين-أ": "https://i.imgur.com/iT3eULe.jpg",
    "أكني فري": "https://i.imgur.com/9U8Vxjc.jpg",
    "إيزيس تين ديرم": "https://i.imgur.com/dRkgurZ.jpg"
}
response_text = chat_completion.choices[0].message.content

print("\n🧴 التشخيص والاقتراح:\n" + response_text)

print("\n📸 صور المنتجات المقترحة:")

for name, url in product_images.items():
    if name.lower() in response_text.lower():
        print(f"- {name}: {url}")

print("\n🧴 التشخيص والاقتراح:\n" + chat_completion.choices[0].message.content)

more_help = input("\n💬 هل المنتج مش متوفر وعايز بديل؟ (اكتب نعم أو لا): ").strip().lower()

if more_help == "نعم":
    product_name = input("🧴 اكتب اسم المنتج اللي مش لاقيه: ").strip()

    alt_message = f"""
المنتج التالي غير متوفر في الصيدليات: {product_name}.
اقترح عليّ بدائل متوفرة حاليًا في السوق المصري بنفس الاستخدام أو فعالية قريبة، مع أسمائها التجارية وسعر كل منتج وصورة إن أمكن.
"""

    alt_completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت طبيب أمراض جلدية محترف، هدفك اقتراح بدائل واضحة للمنتجات غير المتوفرة في السوق المصري."},
            {"role": "user", "content": alt_message}
        ]
    )

    print("\n🔄 البدائل المقترحة:\n" + alt_completion.choices[0].message.content)
# طباعة الرد
print("\n🧴 التشخيص والاقتراح:\n" + chat_completion.choices[0].message.content)

# إضافة توصية بالمتابعة
print("\n📅 رجاءً استخدم العلاج لمدة 5-7 أيام حسب تعليمات الاستخدام، وارجع لي بعدها وقلّي إذا حصل تحسن أو ظهرت أعراض جديدة.")
follow_up = input("\n📋 هل استخدمت العلاج؟ هل حصل تحسن أم ظهرت أعراض جديدة؟ (اكتب التفاصيل): ").strip()

if follow_up:
    followup_msg = f"""
مريض استخدم العلاج الموصى به سابقًا، وكتب التالي بعد المتابعة:
"{follow_up}"

⏳ عدّل خطة العلاج حسب المتابعة، وقل إذا استمر على نفس المنتج أو يحتاج تغييره أو إضافة شيء جديد.
"""
    followup_completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت طبيب جلدية تتابع حالة مريض بناءً على الأعراض الجديدة أو التحسن الظاهر، هدفك تعديل خطة العلاج بناءً على تطور الحالة."},
            {"role": "user", "content": followup_msg}
        ]
    )

    print("\n🔁 خطة العلاج بعد المتابعة:\n" + followup_completion.choices[0].message.content)
