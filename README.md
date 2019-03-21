# SpaceCore [![Build Status](https://travis-ci.com/T3CHNOLOG1C/SpaceCore.svg?branch=master)](https://travis-ci.com/T3CHNOLOG1C/SpaceCore)
A modular discord bot written in Python

**Current Release**: 1.0.0

## Features:
- Mostly configurable via configuration file.
- Support for approval system based servers
- Channel lockdowns (including remote lockdowns)
- Join/Leave logs (Toggleable)
- Kick/Ban with logs
- Mute/Unmute
- Generate QR Codes for attachments or URLs
- Warning system (3rd/4th warns kick, 5th bans)
- Addon system

## How to use:
1. Copy `config.py.example` to `config.py`
2. Edit the relevant fields in `config.py`
3. Run `main.py`

## Requirements
- Python 3.6 or later
- [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)
- [pylast](https://github.com/pylast/pylast)
- [qrcode](https://github.com/lincolnloop/python-qrcode)
- [Pillow](https://github.com/python-pillow/Pillow)

## Credits
- [Rapptz](https://github.com/Rapptz) for [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite).
- [astronautlevel](https://github.com/astronautlevel2) for his [QR code addon](https://github.com/astronautlevel2/Discord-Cogs/blob/master/qrgen.py).
