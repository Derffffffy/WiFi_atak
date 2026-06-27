[app]
# Название и данные
title = WiFi Atak
package.name = wifiatak
package.domain = org.arkhip32
source.include_exts = py
source.dir = .
version = 1.0

# Зависимости
requirements = python3,kivy

# Разрешения Android
android.permissions = INTERNET

# Важные настройки для успешной сборки на GitHub
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
# Автоматическое подтверждение лицензии (это уберет ошибку, которая была на скриншоте)
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
# Использование ветки master гарантирует актуальность инструментов
p4a.branch = master
