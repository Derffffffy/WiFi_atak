"""
Простой логгер для аудита действий.
"""
import time
import os

class AppLogger:
    def __init__(self, filename='wifi_audit.log'):
        # Пишем во внутреннюю память приложения
        self._path = os.path.join(
            os.environ.get('EXTERNAL_STORAGE', '/sdcard'),
            filename
        )
    
    def write(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {message}"
        print(line)  # Дублируем в консоль для отладки
        try:
            with open(self._path, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        except Exception as e:
            print(f"Logger error: {e}")
