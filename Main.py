from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.utils import get_color_from_hex

class VPNApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=30, spacing=20, **kwargs)
        Window.clearcolor = get_color_from_hex("#121212")
        
        self.add_widget(Label(text="WiFi Atak", font_size='32sp', color=get_color_from_hex("#00E676"), bold=True))
        self.status = Label(text="Статус: ОТКЛЮЧЕНО", font_size='18sp')
        self.add_widget(self.status)
        
        self.btn = Button(text="ПОДКЛЮЧИТЬ", background_normal='', background_color=get_color_from_hex("#00E676"), size_hint=(1, 0.2))
        self.btn.bind(on_press=self.animate_btn)
        self.add_widget(self.btn)
        self.add_widget(Label(text="arkhip|32", font_size='12sp', color=get_color_from_hex("#666666"), size_hint=(1, 0.1)))

    def animate_btn(self, instance):
        if self.btn.text == "ПОДКЛЮЧИТЬ":
            self.btn.text = "ОТКЛЮЧИТЬ"
            self.btn.background_color = get_color_from_hex("#FF5252")
            self.status.text = "Статус: АКТИВНО"
        else:
            self.btn.text = "ПОДКЛЮЧИТЬ"
            self.btn.background_color = get_color_from_hex("#00E676")
            self.status.text = "Статус: ОТКЛЮЧЕНО"

class CyberApp(App):
    def build(self):
        return VPNApp()

if __name__ == '__main__':
    CyberApp().run()
    
