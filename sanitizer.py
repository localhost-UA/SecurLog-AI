import re

class LogSanitizer:
    def __init__(self):
        # Регулярні вирази для пошуку чутливих даних
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b')
        self.user_pattern = re.compile(r'(user|login)[=:\s]+([a-zA-Z0-9_\-]+)')

    def sanitize_line(self, log_line: str) -> str:
        """
        Приймає рядок логу та повертає його очищену версію.
        """
        # Приховуємо IP-адреси
        sanitized = self.ip_pattern.sub('[IP_HIDDEN]', log_line)
        
        # Приховуємо MAC-адреси
        sanitized = self.mac_pattern.sub('[MAC_HIDDEN]', sanitized)
        
        # Приховуємо імена користувачів, зберігаючи префікс
        sanitized = self.user_pattern.sub(r'\1=[USER_HIDDEN]', sanitized)
        
        return sanitized