# SPDX-FileCopyrightText: 2024 Eric Z. Ayers
#
# SPDX-License-Identifier: Creative Commons Zero 1.0

"""Control a SONOS speaker to mute/unmute it """

import board
import busio
import ipaddress
import microcontroller
import os
import socketpool
import time
import wifi

import adafruit_connection_manager
import adafruit_requests

##################
# *EDIT*

# Here is a nasty way that might work:
# https://null-byte.wonderhowto.com/how-to/take-control-sonos-iot-devices-with-python-0191144/

#
# We are going to mute / unmute using this command:
# https://docs.sonos.com/reference/playervolume-setmute-playerid
#
# curl --request POST \
#     --url https://api.ws.sonos.com/control/api/v1/players/playerId/playerVolume/mute \
#     --header 'accept: application/json' \
#     --header 'content-type: application/json' \
#     --data '{"muted":true}'
#
#
# Authorization OAuth2+2:
# Bearer token
# token
# X-Sonos-Api-Key
#

MUTE_POST_URL = (
    "https://api.ws.sonos.com/control/api/v1/players/{playerId}/playerVolume/mute"
)


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


def ping_nameserver():
    #  pings Google DNS server to test connectivity
    ipv4 = ipaddress.ip_address("8.8.4.4")
    print(" Internet up. Ping to google.com in: %f ms" % (wifi.radio.ping(ipv4) * 1000))


def connect_to_wifi():
    ssid = secrets["wifi_ssid"]

    print()
    print("Connecting to WiFi network: ", ssid)

    wifi.radio.connect(ssid, secrets["wifi_password"])

    #  prints IP address to REPL
    print("  Connected: IP address ", wifi.radio.ipv4_address, end="")


def reset_uc(e):
    print("  Error:\n", str(e), "Resetting microcontroller in 10 seconds")
    time.sleep(10)
    microcontroller.reset()

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# print(f"\nConnecting to {ssid}...")
# print(f"Signal Strength: {rssi}")

try:
    connect_to_wifi()
except Exception as e:
    reset_uc(e)

while True:
    time.sleep(1)
    try:
        ping_nameserver()
    except Exception as e:
        reset_uc(e)
    time.sleep(10)

# An example POST request
DATA = "This is an example of a JSON value"
print(f" | ✅ JSON 'value' POST Test: {JSON_POST_URL} {DATA}")
with requests.post(JSON_POST_URL, data=DATA) as response:
    json_resp = response.json()
    # Parse out the 'data' key from json_resp dict.
    print(f" | ✅ JSON 'value' Response: {json_resp['data']}")
print("-" * 80)

print("Finished!")
