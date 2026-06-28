"""
Ядро WiFi анализатора: сканер, OUI, пароли, рекомендации.
Объединено в один файл для совместимости с Pydroid.
"""
import time
from kivy.utils import platform

# --- Локальная OUI база (производители по MAC) ---
OUI_DB = {
    'F0:9F:C2': 'Ubiquiti',
    'FC:EC:DA': 'Ubiquiti',
    'D4:6E:35': 'Huawei',
    'B4:0C:25': 'Samsung',
    '00:1A:2B': 'Intel',
    '00:1B:63': 'Apple',
    'A4:83:E7': 'Apple',
    '00:11:22': 'Cisco',
    'C0:25:A2': 'TP-Link',
    'E0:CB:BC': 'ASUS',
    'A4:2B:8C': 'Xiaomi',
    '70:4C:A5': 'D-Link',
    '14:CC:20': 'Netgear',
    '00:1C:DF': 'Belkin',
    'B0:BE:76': 'Tenda',
    'C8:D7:19': 'ZTE',
    '78:44:76': 'Zyxel',
    '00:25:9C': 'Linksys',
    '58:EF:68': 'Xiaomi',
    'A4:91:B1': 'Microsoft',
}

# --- Типовые SSID роутеров (часто с паролем по умолчанию) ---
DEFAULT_SSID_PATTERNS = [
    'TP-Link', 'tp-link', 'Tenda', 'tenda', 'ASUS', 'asus',
    'D-Link', 'dlink', 'NETGEAR', 'netgear', 'ZyXEL', 'zyxel',
    'Xiaomi', 'xiaomi', 'Huawei', 'huawei', 'Keenetic',
    'MGTS', 'Beeline', 'Rostelecom', 'RT-WiFi',
    'DIR-', 'TL-WR', 'default', 'setup', 'F0:9F:C2',
]

# --- Топ-50 слабых паролей ---
WEAK_PASSWORDS = [
    '12345678', 'password', '123456789', '12345', '1234567890',
    'qwerty', 'admin', 'wifi', '1234567', '11111111',
    '123123', 'abc123', 'letmein', 'monkey', 'dragon',
    'master', '1234', '00000000', '88888888', 'iloveyou',
    'password1', 'qwerty123', 'football', 'baseball', 'welcome',
    'sunshine', 'princess', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
    'passw0rd', '123321', '654321', '7777777', '121212',
    'qazwsx', 'password123', '1q2w3e4r', '123qwe', 'qwe123',
    'changeme', 'secret', '123abc', 'abcde', 'loveyou',
]

class WiFiCore:
    """Основной класс: сканирование, анализ, рекомендации"""
    
    def __init__(self):
        self._wifi_manager = None
        if platform == 'android':
            try:
                from jnius import autoclass, cast
                Context = autoclass('android.content.Context')
                WifiManager = autoclass('android.net.wifi.WifiManager')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                act = PythonActivity.mActivity
                self._wifi_manager = cast(WifiManager, act.getSystemService(Context.WIFI_SERVICE))
            except Exception as e:
                print(f"WiFiCore: не удалось получить WifiManager: {e}")
    
    # ----------------------------------------------------------------
    # Сканирование
    # ----------------------------------------------------------------
    def scan(self):
        """Возвращает список словарей с информацией о сетях"""
        if self._wifi_manager is None:
            return self._demo_scan()
        
        networks = []
        
        # Включаем Wi-Fi если выключен
        if not self._wifi_manager.isWifiEnabled():
            self._wifi_manager.setWifiEnabled(True)
            time.sleep(2)
        
        self._wifi_manager.startScan()
        time.sleep(1.8)
        
        for r in self._wifi_manager.getScanResults():
            net = {
                'ssid':        r.SSID if r.SSID else '<скрыта>',
                'bssid':       r.BSSID if r.BSSID else '',
                'rssi':        r.level,
                'channel':     self._freq_to_channel(r.frequency),
                'encryption':  self._parse_encryption(r.capabilities),
                'wps':         self._has_wps(r.capabilities),
                'weak_password': self._guess_default_password(r.SSID if r.SSID else ''),
                'vendor':      self._oui_lookup(r.BSSID if r.BSSID else ''),
                'frequency':   r.frequency,
                'timestamp':   time.time(),
            }
            networks.append(net)
        
        return networks
    
    def _freq_to_channel(self, freq):
        if freq == 0: return 0
        if 2412 <= freq <= 2484:
            return (freq - 2412) // 5 + 1
        if 5180 <= freq <= 5825:
            return (freq - 5180) // 5 + 36
        return 0
    
    def _parse_encryption(self, caps):
        if not caps: return 'Unknown'
        if 'WPA3' in caps: return 'WPA3'
        if 'WPA2' in caps: return 'WPA2'
        if 'WPA' in caps:  return 'WPA'
        if 'WEP' in caps:  return 'WEP'
        if '[ESS]' in caps: return 'Open'
        return 'Unknown'
    
    def _has_wps(self, caps):
        if not caps: return False
        return 'WPS' in caps.upper()
    
    # ----------------------------------------------------------------
    # OUI lookup
    # ----------------------------------------------------------------
    def _oui_lookup(self, mac):
        if not mac or len(mac) < 8:
            return 'Неизвестно'
        prefix = mac.upper()[:8]
        return OUI_DB.get(prefix, f'Неизв. ({mac[:8]})')
    
    # ----------------------------------------------------------------
    # Угадывание пароля по умолчанию
    # ----------------------------------------------------------------
    def _guess_default_password(self, ssid):
        if not ssid: return False
        ssid_lower = ssid.lower()
        for pat in DEFAULT_SSID_PATTERNS:
            if pat.lower() in ssid_lower:
                return True
        return False
    
    # ----------------------------------------------------------------
    # Проверка пароля пользователя
    # ----------------------------------------------------------------
    def check_password(self, password):
        """Возвращает {'strong': bool, 'reason': str, 'crack_time': str}"""
        if not password:
            return {'strong': False, 'reason': 'Пустой пароль', 'crack_time': '-'}
        
        if password.lower() in WEAK_PASSWORDS:
            return {
                'strong': False,
                'reason': 'В списке 50 самых слабых паролей',
                'crack_time': 'Мгновенно'
            }
        
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        score = sum([has_upper, has_lower, has_digit, has_special])
        
        if length >= 12 and score >= 3:
            return {'strong': True, 'reason': 'Надёжный', 'crack_time': 'Годы'}
        elif length >= 8 and score >= 2:
            return {'strong': False, 'reason': 'Средний', 'crack_time': '~1 день'}
        else:
            return {'strong': False, 'reason': 'Слишком простой', 'crack_time': 'Секунды'}
    
    # ----------------------------------------------------------------
    # Рекомендации
    # ----------------------------------------------------------------
    def get_tips(self, net):
        tips = []
        enc = net.get('encryption', '')
        if enc in ('WEP', 'Open'):
            tips.append('СРОЧНО: смените шифрование на WPA2/WPA3')
        if net.get('wps'):
            tips.append('Отключите WPS в настройках роутера')
        if net.get('weak_password'):
            tips.append('Смените стандартный пароль на уникальный')
        if enc == 'WPA2':
            tips.append('По возможности обновите роутер до WPA3')
        if not tips:
            tips.append('Сеть настроена хорошо')
        return tips
    
    # ----------------------------------------------------------------
    # Демо-данные (для тестов на ПК)
    # ----------------------------------------------------------------
    def _demo_scan(self):
        return [
            {
                'ssid': 'Home_5G', 'bssid': 'F0:9F:C2:AA:BB:CC',
                'rssi': -42, 'channel': 36, 'encryption': 'WPA3',
                'wps': False, 'weak_password': False,
                'vendor': 'Ubiquiti', 'timestamp': time.time()
            },
            {
                'ssid': 'TP-Link_Cafe', 'bssid': 'C0:25:A2:DD:EE:FF',
                'rssi': -65, 'channel': 6, 'encryption': 'WPA2',
                'wps': True, 'weak_password': True,
                'vendor': 'TP-Link', 'timestamp': time.time()
            },
            {
                'ssid': 'OldRouter', 'bssid': '00:1C:DF:11:22:33',
                'rssi': -78, 'channel': 11, 'encryption': 'WEP',
                'wps': True, 'weak_password': True,
                'vendor': 'Belkin', 'timestamp': time.time()
            },
            {
                'ssid': 'Free_Hotspot', 'bssid': '14:CC:20:44:55:66',
                'rssi': -55, 'channel': 1, 'encryption': 'Open',
                'wps': False, 'weak_password': False,
                'vendor': 'Netgear', 'timestamp': time.time()
            },
              ]
