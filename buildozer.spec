[app]
title = WiFi_atak
package.name = wifiatak
package.domain = org.test
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Используем 32-битную архитектуру — она легче и универсальнее
archs = armeabi-v7a
# Указываем правильные разрешения для работы с Wi-Fi
permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
