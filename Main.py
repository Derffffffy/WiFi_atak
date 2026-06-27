from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.utils import get_color_from_hex

COLORS = {
    'bg': get_color_from_hex("#121212"),
    'accent': get_color_from_hex("#00E676"),
    'danger': get_color_from_hex("#FF5252"),
    'text': get_color_from_hex("#FFFFFF"),
    'footer': get_color_from_hex("#666666")
}

class VPNApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=30, spacing=20, **kwargs)
        Window.clearcolor = COLORS['bg']
        
        # Заголовок
        self.add_widget(Label(text="WiFi Atak", font_size='32sp', color=COLORS['accent'], bold=True))
        
        # Статус
        self.status = Label(text="Статус: ОТКЛЮЧЕНО", font_size='18sp', color=COLORS['text'])
        self.add_widget(self.status)
        
        # Кнопка
        self.btn = Button(text="ПОДКЛЮЧИТЬ", background_normal='', background_color=COLORS['accent'], size_hint=(1, 0.2))
        self.btn.bind(on_press=self.animate_btn)
        self.add_widget(self.btn)
        
        # Подпись автора
        self.add_widget(Label(text="arkhip|32", font_size='12sp', color=COLORS['footer'], size_hint=(1, 0.1)))

    def animate_btn(self, instance):
        anim = Animation(size=(self.btn.width * 0.95, self.btn.height * 0.95), duration=0.1) + \
               Animation(size=(self.btn.width, self.btn.height), duration=0.1)
        anim.start(self.btn)
        
        if self.btn.text == "ПОДКЛЮЧИТЬ":
            self.btn.text = "ОТКЛЮЧИТЬ"
            self.btn.background_color = COLORS['danger']
            self.status.text = "Статус: ЗАЩИТА АКТИВНА"
        else:
            self.btn.text = "ПОДКЛЮЧИТЬ"
            self.btn.background_color = COLORS['accent']
            self.status.text = "Статус: ОТКЛЮЧЕНО"

class CyberApp(App):
    def build(self):
        return VPNApp()

if __name__ == '__main__':
    CyberApp().run()
    
