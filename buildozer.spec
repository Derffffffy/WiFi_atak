[app]
# Название и данные
title = WiFi Atak
package.name = wifiatak
package.domain = org.arkhip32
source.include_exts = py,png
version = 1.0

# Минимально необходимые зависимости для стабильности
requirements = python3,kivy

# Разрешения Android
android.permissions = INTERNET

# Настройки API (33 — стандарт для актуальных версий Android)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Иконка (раскомментируй, если положишь файл icon.png в репозиторий)
icon.filename = %(source.dir)s/icon.png

# Дополнительные настройки для стабильности сборки
[buildozer]
log_level = 2
warn_on_root = 1
# Прямая ветка для корректной сборки линкера
p4a.branch = master

