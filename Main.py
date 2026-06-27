from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

class WiFiAtakApp(App):
    def build(self):
        # Проверка прав доступа при запуске
        return Label(text="WiFi Atak инициализирован\nОжидание реализации логики")

if __name__ == '__main__':
    WiFiAtakApp().run()
    
