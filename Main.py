from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton

class WiFiAtakApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        screen.add_widget(MDLabel(text="WiFi Atak v0.1", halign="center", pos_hint={"center_y": 0.8}))
        screen.add_widget(MDFloatingActionButton(icon="wifi", pos_hint={"center_x": 0.5, "center_y": 0.5}, on_release=self.run_logic))
        return screen

    def run_logic(self, instance):
        # Здесь мы позже добавим вызов системных функций
        pass

if __name__ == '__main__':
    WiFiAtakApp().run()
    
