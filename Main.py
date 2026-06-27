from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="WiFi Atak готова к работе", halign="center"))
        self.btn = MDFloatingActionButton(icon="wifi", pos_hint={"center_x": 0.5, "center_y": 0.2})
        self.btn.bind(on_release=self.start_scan)
        self.add_widget(self.btn)

    def start_scan(self, *args):
        # Здесь будет логика сканирования
        print("Сканирование запущено...")

class WiFiAtakApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MainScreen()

if __name__ == '__main__':
    WiFiAtakApp().run()
    
