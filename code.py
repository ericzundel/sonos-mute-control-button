# SPDX-FileCopyrightText: 2024 Eric Z. Ayers
#
# SPDX-License-Identifier: Creative Commons Zero 1.0

"""Collect training data from a color sensor and publish it to Adafruit IO """

import board
import busio
import ipaddress
import os
import socketpool
import time
import wifi


##################
# *EDIT*

#
# End of editable config values
##################

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print(
        "WiFi secrets are kept in secrets.py, please add them there and don't commit them to git!"
    )
    raise

def ping_namserver():
    #  pings Google DNS server to test connectivity
    ipv4 = ipaddress.ip_address("8.8.4.4")
    print(
        " Internet up. Ping to google.com in: %f ms"
        % (wifi.radio.ping(ipv4) * 1000)
    )

def connect_to_wifi():
    print()
    print("Connecting to WiFi...", end="")

    wifi.radio.connect(secrets["wifi_ssid"], secrets["wifi_password"])

    #  prints IP address to REPL
    print("Connected: IP address %s", wifi.radio.ipv4_address, end="")



connect_to_wifi()

while True:
    time.sleep(1)
    ping_namserver()
    time.sleep(10)
