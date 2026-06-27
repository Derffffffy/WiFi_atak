[app]
title = WiFi Atak
package.name = wifiatak
package.domain = org.test
source.dir = .
source.include_exts = py,kv
version = 0.1
requirements = python3,kivy,kivymd,jnius
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools_version = 33.0.1
android.ndk = 25b
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
