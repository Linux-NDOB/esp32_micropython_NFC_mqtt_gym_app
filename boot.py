# This file is executed on every boot (including wake-boot from deepsleep)
import network
import esp
import gc
esp.osdebug(None)
gc.collect()

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('ssid', 'password')


