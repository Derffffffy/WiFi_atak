from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window

class WiFiAtakApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark" # Темная тема, как у VPN
        screen = MDScreen()
        
        # Заголовок
        self.label = MDLabel(text="WiFi Atak: Статус - Отключен", halign="center", pos_hint={"center_y": 0.7})
        
        # Большая кнопка (как в VPN)
        self.button = MDFloatingActionButton(
            icon="wifi",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.toggle_status
        )
        
        screen.add_widget(self.label)
        screen.add_widget(self.button)
        return screen

    def toggle_status(self, instance):
        if self.label.text == "WiFi Atak: Статус - Отключен":
            self.label.text = "WiFi Atak: Сканирование..."
            self.button.md_bg_color = (0, 1, 0, 1) # Зеленый при включении
        else:
            self.label.text = "WiFi Atak: Статус - Отключен"
            self.button.md_bg_color = (1, 0, 0, 1) # Красный при выключении

if __name__ == '__main__':
    WiFiAtakApp().run()
    
