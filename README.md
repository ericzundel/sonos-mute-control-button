# One Button Remote for SONOS bar mute

This project uses CircuitPython on a microcontroller to 
implement a one-button remote to mute/unmute the Sonos bar.


## SONOS Developer Portal

Sign up for a developer account here:
https://integration.sonos.com/users/sign_up

## Sonos Control API

Use the API to Mute / unmute using this command:
https://docs.sonos.com/reference/playervolume-setmute-playerid

curl --request POST \
     --url https://api.ws.sonos.com/control/api/v1/players/playerId/playerVolume/mute \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"muted":true}'


Authorization OAuth2+2:
Bearer token
token
X-Sonos-Api-Key


