import streamlit as st
from ai_functions import main_ai_function, generate_image

st.set_page_config(page_title="AI Project Architect", page_icon="🚀", layout="wide")

tab1, tab2, tab3 = st.tabs(["Головна", "AI-моделі", "Аналіз ідеї"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🚀 AI Project Architect")
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.subheader("Перетвори свою ідею на цілісну структуру проєкту за допомогою штучного інтелекту")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Аналіз ідеї")
        st.write("Введи свою ідею або завантаж зображення, щоб AI зрозумів, який проєкт ти хочеш створити.")
    with col2:
        st.subheader("Оцінка проєкту")
        st.write("AI визначить основні функції проєкту та допоможе зрозуміти, як його краще організувати.")
    with col3:
        st.subheader("Структура проєкту")
        st.write("Отримай готову структуру свого проєкту з основними компонентами та їхнім описом.")

with tab2:
    st.title("Моделі штучного інтелекту") 
    model = st.selectbox("Обери AI-модель", ["Gemini", "Hugging Face"]) 
    st.subheader(f"Обрана модель: {model}") 
    if model == "Gemini": 
        st.write(f"{model} - це передовий мультимодальний штучний інтелект від Google, який здатен одночасно розуміти, аналізувати та створювати текст, код, зображення, аудіо та відео.") 
    else: 
        st.write(f"{model} - це платформа штучного інтелекту, яка дає безкоштовний доступ до величезної бази готових нейромереж і дозволяє мені в один клік вибрати потрібну модель для перекладу, генерації тексту, розпізнавання мови або роботи із зображеннями.")

with tab3:
    st.title("Середовище аналізу проєкту") 
    prompt = st.text_area("Опиши свою ідею")
    project_type = st.selectbox("Тип проєкту", ["Вебзастосунок", "Мобільний застосунок", "Комп'ютерна програма", "Гра", "Інше"])
    answer_size = st.selectbox("Розмір відповіді AI", ["Коротка", "Середня", "Розгорнута"])
    language = st.radio("Оберіть мову відповіді AI", ["Українська", "Англійська"])

    if st.button("Створити структуру"):
        if not prompt.strip():
            st.warning("Спочатку опиши ідею проєкту і повтори спробу.")
        else:
            with st.spinner(f"{model} створює структуру вашого проєкту..."):
                result, error = main_ai_function(prompt, model, project_type, answer_size, language)
            if error:
                st.error(error)
            else:
                st.session_state["project_result"] = result

    if "project_result" in st.session_state:
        st.subheader("Структура проєкту")
        st.markdown(st.session_state["project_result"])
        st.download_button("Завантажити структуру", data=st.session_state["project_result"],
                                                    file_name="project_structure.md", 
                                                    mime="text/markdown")

    st.divider()
    st.subheader("Генерація зображення")
    image_prompt = st.text_area("Опиши зображення, яке потрібно створити")
    reference_image = st.file_uploader("Референсне зображення (необов'язково)", type=["jpg", "jpeg", "png"])

    if reference_image:
        st.image(reference_image, caption="Референсне зображення")

    if st.button("Згенерувати зображення"):
        if not image_prompt.strip():
            st.warning("Введи опис зображення.")
        else:
            with st.spinner("Hugging Face генерує зображення..."):
                image_bytes, error = generate_image(image_prompt, reference_image)
            if error:
                st.error(error)
            else:
                st.session_state["last_image"] = image_bytes

    if "last_image" in st.session_state:
        st.image(st.session_state["last_image"], caption="Згенероване зображення", use_container_width=True)
        st.download_button("Завантажити зображення",
                            data=st.session_state["last_image"], 
                            file_name="generated_image.png", 
                            mime="image/png")
