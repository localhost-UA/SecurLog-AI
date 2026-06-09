@echo off
chcp 65001 >nul

echo ==============================================
echo   Запуск SecurLog AI (Ожидайте...)
echo ==============================================

echo [1/2] Запуск локального сервера ИИ...
start /b ollama serve >nul 2>&1
timeout /t 3 /nobreak > NUL

echo [2/2] Запуск веб-интерфейса в браузере...
python -m streamlit run app.py

pause