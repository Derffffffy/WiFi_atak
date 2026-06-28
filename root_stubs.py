"""
Заглушки root-функций с проверкой доступности.
"""
import os

class RootChecker:
    @staticmethod
    def is_available():
        try:
            result = os.popen('su -c id 2>/dev/null').read()
            return 'uid=0' in result
        except:
            return False

class RootActions:
    def __init__(self):
        self.has_root = RootChecker.is_available()
    
    def deauth(self, bssid, client='FF:FF:FF:FF:FF:FF', count=10):
        if not self.has_root:
            return False, "Требуется root"
        cmd = f"su -c 'aireplay-ng -0 {count} -a {bssid} -c {client} wlan0'"
        print(f"[root] {cmd}")
        return True, "Deauth запущен"
    
    def pmkid_capture(self, interface='wlan0'):
        if not self.has_root:
            return False, "Требуется root"
        cmd = f"su -c 'hcxdumptool -i {interface} -o /sdcard/pmkid.pcapng --enable_status=1'"
        print(f"[root] {cmd}")
        return True, "Захват PMKID запущен"
    
    def monitor_mode(self, interface='wlan0'):
        if not self.has_root:
            return False, "Требуется root"
        cmds = [
            f"su -c 'ip link set {interface} down'",
            f"su -c 'iw {interface} set monitor control'",
            f"su -c 'ip link set {interface} up'",
        ]
        for c in cmds:
            print(f"[root] {c}")
        return True, "Мониторный режим включён"
    
    def emergency_kill(self):
        os.system("su -c 'killall -9 aireplay-ng airodump-ng hcxdumptool 2>/dev/null'")
        return True
