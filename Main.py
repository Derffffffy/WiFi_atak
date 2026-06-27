from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class WiFiAtakApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MDScreen(MDLabel(text="WiFi Atak v0.1: Сборка успешна", halign="center"))

if __name__ == '__main__':
    WiFiAtakApp().run()
    
