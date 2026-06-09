import json
import requests

class LocalAIAnalyzer:
    def __init__(self, model_name: str = "phi3"):
        self.api_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
        
        # Системний промпт українською мовою
        self.system_prompt = (
            "Ти — суворий AI-аналітик мережевої безпеки. "
            "Твоя задача — проаналізувати рядок логу і повернути ТІЛЬКИ валідний JSON. "
            "Всі описи та рекомендації пиши українською мовою. "
            "Формат відповіді: {\"severity\": \"Low/Medium/High/Critical\", \"issue\": \"короткий опис проблеми\", \"recommendation\": \"що конкретно зробити\"}. "
            "Не пиши жодних вступів та пояснень, видавай лише JSON."
        )

    def analyze_log(self, sanitized_log: str) -> dict:
        payload = {
            "model": self.model_name,
            "prompt": f"{self.system_prompt}\n\nЛог для аналізу: {sanitized_log}",
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            ai_text = response.json().get("response", "")
            return json.loads(ai_text)
            
        except requests.exceptions.RequestException:
            return {
                "severity": "Error",
                "issue": "Помилка зв'язку з локальним ШІ (Ollama)",
                "recommendation": "Перевірте, чи запущено команду 'ollama run phi3'"
            }
        except json.JSONDecodeError:
             return {
                "severity": "Error",
                "issue": "ШІ повернув некоректний формат даних",
                "recommendation": "Спробуйте перезапустити аналіз"
            }