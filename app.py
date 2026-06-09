import streamlit as st
import pandas as pd
import time
from sanitizer import LogSanitizer
from ai_analyzer import LocalAIAnalyzer

# Налаштування сторінки
st.set_page_config(page_title="SecurLog AI", page_icon="🛡️", layout="wide")

# Заголовки
st.title("🛡️ SecurLog Local AI")
st.markdown("**Автоматичний та безпечний аналіз системних журналів (Privacy First)**")
st.markdown("Усі дані обробляються виключно на цьому комп'ютері. Жоден байт не передається в інтернет.")

# Ініціалізація модулів
@st.cache_resource
def load_modules():
    return LogSanitizer(), LocalAIAnalyzer()

sanitizer, analyzer = load_modules()

# Віджет завантаження файлу
uploaded_file = st.file_uploader("Завантажте файл з логами (.txt або .log)", type=['txt', 'log'])

if uploaded_file is not None:
    # Читаємо файл
    string_data = uploaded_file.getvalue().decode("utf-8")
    logs = string_data.splitlines()
    
    # Видаляємо порожні рядки
    logs = [line for line in logs if line.strip()]
    
    st.info(f"📁 Файл завантажено. Знайдено рядків для аналізу: {len(logs)}")
    
    if st.button("🚀 Розпочати аналіз", type="primary"):
        # Підготовка таблиці та прогрес-бару
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        
        # Обробка кожного рядка
        for i, line in enumerate(logs):
            safe_log = sanitizer.sanitize_line(line)
            status_text.markdown(f"**ШІ аналізує:** `{safe_log[:60]}...`")
            
            # Аналіз нейромережею
            ai_result = analyzer.analyze_log(safe_log)
            
            # Зберігаємо результати
            results.append({
                "Статус": ai_result.get('severity', 'Unknown'),
                "Анонімізований Лог": safe_log,
                "Вердикт ШІ": ai_result.get('issue', '-'),
                "Рекомендація": ai_result.get('recommendation', '-')
            })
            
            # Оновлюємо прогрес-бар
            progress_bar.progress((i + 1) / len(logs))
            time.sleep(0.1) # Невелика пауза для стабільності
            
        status_text.success("✅ Аналіз успішно завершено!")
        
        # Створюємо красиву таблицю (Dataframe)
        df = pd.DataFrame(results)
        
        # Функція для підсвічування статусів
        def highlight_severity(val):
            color = 'black'
            if val in ['Critical', 'High']: color = '#ff4b4b'
            elif val == 'Medium': color = '#ffa421'
            elif val == 'Low': color = '#21c354'
            return f'color: {color}; font-weight: bold'
        
        # Виводимо таблицю
        st.dataframe(
            df.style.map(highlight_severity, subset=['Статус']),
            use_container_width=True,
            hide_index=True
        )