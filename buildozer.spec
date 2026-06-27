[app]
title = WiFi Atak
package.name = wifiatak
package.domain = org.arkhip32
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy
android.permissions = INTERNET
# Принудительно принимаем лицензии
android.accept_sdk_license = True
# Указываем конкретные версии для стабильности
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
