"""
WiFi Analyzer - основное приложение
Сборка: Pydroid 3 -> Меню -> Экспорт в APK
Все импорты локальные (файлы лежат рядом)
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

# Локальные модули (лежат рядом с этим файлом)
from wifi_core import WiFiCore
from logger_app import AppLogger
from root_stubs import RootChecker, RootActions

import threading

# Цвета для кнопок сетей
C_RED    = (0.95, 0.25, 0.25, 1)   # WEP / Open / WPS
C_YELLOW = (1.00, 0.80, 0.00, 1)   # WPA2 + слабый пароль
C_GREEN  = (0.20, 0.75, 0.25, 1)   # WPA3 / надёжно
C_GRAY   = (0.45, 0.45, 0.45, 1)   # Неизвестно
C_BLUE   = (0.20, 0.55, 0.95, 1)   # Кнопки действий

class MainApp(App):
    """Главный класс приложения Kivy"""
    
    def build(self):
        self.title = 'WiFi Analyzer'
        self.logger = AppLogger()
        self.logger.write("Приложение запущено")
        
        # Проверка root один раз
        self.root_ok = RootChecker.is_available()
        self.logger.write(f"Root доступ: {self.root_ok}")
        
        # Показываем предупреждение через 0.5 сек после старта
        Clock.schedule_once(self._show_disclaimer, 0.5)
        
        return MainScreen(root_ok=self.root_ok, logger=self.logger)
    
    def _show_disclaimer(self, dt):
        text = (
            "Данное приложение предназначено ТОЛЬКО для "
            "тестирования СОБСТВЕННЫХ сетей.\n\n"
            "Использование против чужих сетей незаконно.\n"
            "Все действия логируются локально."
        )
        popup = Popup(
            title='ПРЕДУПРЕЖДЕНИЕ',
            content=Label(text=text, padding=16, halign='left', valign='top'),
            size_hint=(0.88, 0.42)
        )
        popup.content.bind(size=popup.content.setter('text_size'))
        popup.open()
        Clock.schedule_once(popup.dismiss, 6)

class MainScreen(BoxLayout):
    """Главный экран приложения"""
    
    def __init__(self, root_ok=False, logger=None, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=8, **kwargs)
        
        self.root_ok = root_ok
        self.logger = logger
        self.wifi = WiFiCore()
        self.networks = []
        self._scan_event = None
        
        # --- Заголовок ---
        self.add_widget(Label(
            text='WiFi Analyzer',
            size_hint_y=0.08,
            font_size=26,
            bold=True,
            color=(0.9, 0.9, 1, 1)
        ))
        
        # --- Статус root ---
        root_text = 'Root: ДА (расширенный)' if root_ok else 'Root: НЕТ (базовый)'
        root_color = C_GREEN if root_ok else C_GRAY
        self.add_widget(Label(
            text=root_text, size_hint_y=0.04, font_size=12, color=root_color
        ))
        
        # --- Кнопки сканирования и стопа ---
        btns = GridLayout(cols=2, spacing=8, size_hint_y=0.12)
        
        self.btn_scan = Button(
            text='СКАНИРОВАТЬ СЕТИ',
            background_color=C_BLUE,
            bold=True
        )
        self.btn_scan.bind(on_press=self._start_scan)
        btns.add_widget(self.btn_scan)
        
        self.btn_stop = Button(
            text='АВАРИЙНЫЙ СТОП',
            background_color=(1, 0.15, 0.15, 1),
            bold=True
        )
        self.btn_stop.bind(on_press=self._emergency_stop)
        btns.add_widget(self.btn_stop)
        
        self.add_widget(btns)
        
        # --- Статусная строка ---
        self.lbl_status = Label(
            text='Нажмите "Сканировать сети"',
            size_hint_y=0.05, font_size=13
        )
        self.add_widget(self.lbl_status)
        
        # --- Список сетей (прокручиваемый) ---
        self.net_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.net_container.bind(minimum_height=self.net_container.setter('height'))
        
        scroll = ScrollView(size_hint_y=0.65)
        scroll.add_widget(self.net_container)
        self.add_widget(scroll)
    
    def _start_scan(self, instance):
        """Запуск сканирования (в фоновом потоке)"""
        self.btn_scan.disabled = True
        self.lbl_status.text = 'Сканирование...'
        self.logger.write("Сканирование запущено")
        
        threading.Thread(target=self._scan_thread, daemon=True).start()
        
        # Автообновление каждые 5 секунд
        if self._scan_event:
            self._scan_event.cancel()
        self._scan_event = Clock.schedule_interval(lambda dt: self._refresh(), 5)
    
    def _scan_thread(self):
        """Фоновый поток сканирования"""
        try:
            self.networks = self.wifi.scan()
            self.logger.write(f"Найдено сетей: {len(self.networks)}")
            Clock.schedule_once(lambda dt: self._update_list())
        except Exception as e:
            self.logger.write(f"Ошибка сканирования: {e}")
            Clock.schedule_once(lambda dt: self._show_error(str(e)))
    
    def _refresh(self):
        """Повторное сканирование без блокировки кнопки"""
        threading.Thread(target=self._scan_thread, daemon=True).start()
    
    def _update_list(self):
        """Обновление списка сетей на экране"""
        self.btn_scan.disabled = False
        self.net_container.clear_widgets()
        
        if not self.networks:
            self.lbl_status.text = 'Сети не найдены'
            return
        
        self.lbl_status.text = f'Найдено: {len(self.networks)} сетей'
        
        # Сортируем по уровню сигнала (лучшие сверху)
        for net in sorted(self.networks, key=lambda n: n.get('rssi', -100), reverse=True):
            btn = self._make_net_button(net)
            self.net_container.add_widget(btn)
    
    def _make_net_button(self, net):
        """Создаёт кнопку сети с цветовой индикацией"""
        enc = net.get('encryption', '')
        wps = net.get('wps', False)
        weak = net.get('weak_password', False)
        
        if enc in ('WEP', 'Open') or wps:
            color = C_RED
        elif enc == 'WPA2' and weak:
            color = C_YELLOW
        elif enc == 'WPA3':
            color = C_GREEN
        else:
            color = C_GRAY
        
        btn = Button(
            text=f"[{enc}] {net.get('ssid', '?')}   {net.get('rssi', 0)} dBm",
            background_color=color,
            size_hint_y=None,
            height=48,
            halign='left',
            valign='middle'
        )
        btn.bind(size=btn.setter('text_size'))
        btn.bind(on_press=lambda instance, n=net: self._show_details(n))
        return btn
    
    def _show_details(self, net):
        """Карточка сети с кнопками тестов"""
        content = GridLayout(cols=1, spacing=6, padding=12, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Информация
        info = [
            f"SSID: {net.get('ssid', '-')}",
            f"BSSID: {net.get('bssid', '-')}",
            f"Сигнал: {net.get('rssi', 0)} dBm",
            f"Канал: {net.get('channel', 0)}",
            f"Шифрование: {net.get('encryption', '?')}",
            f"Производитель: {net.get('vendor', '?')}",
            f"WPS: {'ДА (опасно)' if net.get('wps') else 'Нет'}",
            f"Пароль по умолчанию: {'ВОЗМОЖНО' if net.get('weak_password') else 'Нет'}",
        ]
        for line in info:
            lbl = Label(text=line, size_hint_y=None, height=30, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            content.add_widget(lbl)
        
        # Кнопка проверки пароля
        btn_pw = Button(
            text='Проверить пароль (если сеть ваша)',
            size_hint_y=None, height=46,
            background_color=C_BLUE
        )
        btn_pw.bind(on_press=lambda x: self._dialog_check_password(net))
        content.add_widget(btn_pw)
        
        # Кнопки root-функций (если доступен root)
        if self.root_ok:
            btn_deauth = Button(
                text='Deauth-атака [root]',
                size_hint_y=None, height=40,
                background_color=(0.85, 0.35, 0.0, 1)
            )
            btn_deauth.bind(on_press=lambda x: self._dialog_root_action('deauth', net))
            content.add_widget(btn_deauth)
            
            btn_pmkid = Button(
                text='PMKID-захват [root]',
                size_hint_y=None, height=40,
                background_color=(0.75, 0.15, 0.45, 1)
            )
            btn_pmkid.bind(on_press=lambda x: self._dialog_root_action('pmkid', net))
            content.add_widget(btn_pmkid)
        
        # Рекомендации
        tips = self.wifi.get_tips(net)
        if tips:
            for tip in tips[:3]:
                content.add_widget(Label(
                    text=f"• {tip}",
                    size_hint_y=None, height=28,
                    color=(0.7, 0.95, 0.7, 1),
                    halign='left', valign='middle'
                ))
        
        popup = Popup(title='Сеть', content=content, size_hint=(0.9, 0.82))
        popup.open()
    
    def _dialog_check_password(self, net):
        """Диалог проверки пароля"""
        box = BoxLayout(orientation='vertical', spacing=8, padding=10)
        box.add_widget(Label(text='Введите пароль сети:', size_hint_y=None, height=30))
        
        inp = TextInput(password=True, multiline=False, size_hint_y=None, height=42)
        box.add_widget(inp)
        
        result = Label(text='', size_hint_y=None, height=60, halign='left', valign='top')
        result.bind(size=result.setter('text_size'))
        box.add_widget(result)
        
        def check(instance):
            pw = inp.text.strip()
            if not pw:
                result.text = 'Введите пароль'
                return
            res = self.wifi.check_password(pw)
            if res['strong']:
                result.text = 'Надёжный пароль'
                result.color = C_GREEN
            else:
                result.text = f"Слабый: {res.get('reason','?')}\nВзлом: {res.get('crack_time','?')}"
                result.color = C_RED
        
        btn = Button(text='Проверить', size_hint_y=None, height=42, background_color=C_BLUE)
        btn.bind(on_press=check)
        box.add_widget(btn)
        
        Popup(title='Проверка пароля', content=box, size_hint=(0.85, 0.45)).open()
    
    def _dialog_root_action(self, action, net):
        """Диалог с описанием root-функции"""
        texts = {
            'deauth': (
                'Deauth-атака\n\n'
                'Отправляет кадры деавторизации, заставляя клиентов '
                'переподключаться к сети.\n\n'
                'Требует: root + совместимый Wi-Fi чип.\n'
                'Защита: использовать WPA3, отключить 802.11w.'
            ),
            'pmkid': (
                'PMKID-захват\n\n'
                'Получает хэш пароля без активных клиентов '
                'через запрос PMKID у роутера.\n\n'
                'Требует: root + совместимый чип.\n'
                'Защита: отключить Fast Roaming (802.11r).'
            ),
        }
        text = texts.get(action, 'Описание отсутствует')
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        lbl = Label(text=text, halign='left', valign='top')
        lbl.bind(size=lbl.setter('text_size'))
        content.add_widget(lbl)
        content.add_widget(Label(
            text='\n[Функция в разработке]',
            color=C_YELLOW, size_hint_y=None, height=28
        ))
        Popup(title=action.upper(), content=content, size_hint=(0.88, 0.55)).open()
    
    def _emergency_stop(self, instance):
        """Остановка всех фоновых процессов"""
        if self._scan_event:
            self._scan_event.cancel()
            self._scan_event = None
        self.btn_scan.disabled = False
        self.lbl_status.text = 'ВСЕ ПРОЦЕССЫ ОСТАНОВЛЕНЫ'
        self.logger.write("Аварийный стоп")
    
    def _show_error(self, msg):
        """Показ ошибки в статусной строке"""
        self.btn_scan.disabled = False
        self.lbl_status.text = f'Ошибка: {msg[:60]}'

if __name__ == '__main__':
    MainApp().run()
