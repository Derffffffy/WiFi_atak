[app]
title = WiFi_atak
package.name = wifiatak
package.domain = org.test
source.dir = .
source.include_exts = py,kv
version = 0.1
requirements = python3,kivy,kivymd
android.archs = armeabi-v7a
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
