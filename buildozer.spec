[app]
title = WiFi_atak
package.name = wifiatak
package.domain = org.test
# Точка означает, что код лежит в той же папке, что и этот файл
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd
android.archs = armeabi-v7a
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
fullscreen = 0
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
