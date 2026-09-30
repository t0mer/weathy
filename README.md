# weathy

[![Docker Pulls](https://img.shields.io/docker/pulls/techblog/weathy)](https://hub.docker.com/r/techblog/weathy)

weathy is a small Python service that sends a daily weather forecast for a location in Israel at a scheduled time. It pulls the forecast from the Israel Meteorological Service (IMS) through the [weatheril](https://pypi.org/project/weatheril/) library, formats it as a Hebrew message, and delivers it through [Apprise](https://github.com/caronc/apprise). Apprise supports Telegram, which is the main use case (see the screenshot below), plus dozens of other services such as Discord, Slack, Pushover, Gotify and email.

![wathy](https://raw.githubusercontent.com/t0mer/weathy/main/screenshots/wathy.png)

> **Disclaimer:** weathy is an unofficial, community project. It is not affiliated with, endorsed by or connected to the Israel Meteorological Service. All forecast data comes from the IMS; see [ims.gov.il](https://ims.gov.il) for the official forecast and its terms of use.

## Table of contents

- [Features](#features)
- [How it works](#how-it-works)
- [Components and frameworks](#components-and-frameworks)
- [Requirements](#requirements)
- [Create a Telegram bot](#create-a-telegram-bot)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Supported notifications](#supported-notifications)
- [Troubleshooting](#troubleshooting)
- [Security notes](#security-notes)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- Sends one weather forecast per day at a time you choose (`SCHEDULE`).
- Uses IMS forecast data for any location ID that weatheril supports (cities and nature sites, see the [locations table](#locations-table)).
- The message includes:
  - a bold header with the day name and date (`DD/MM/YYYY`);
  - the IMS national forecast text for that day;
  - the day's maximum and minimum temperatures;
  - an hourly list with temperature, weather condition (in Hebrew), and chance of rain. The condition can be empty; see [Troubleshooting](#troubleshooting).
- Delivers the message to one or more [Apprise](https://github.com/caronc/apprise) targets at the same time (Telegram, Discord, Slack, email, and many more).
- If fetching or parsing the forecast fails, sends a short error message (`aw snap something went wrong`) instead, so you know the job ran.
- Runs as a multi-arch Docker image (`linux/amd64`, `linux/arm64`, `linux/arm/v7`).

weathy is a push-only sender. It does not listen for incoming messages, so it has no bot commands and no chat allowlist: it only sends to the targets you list in `NOTIFIERS`.

## How it works

```mermaid
flowchart LR
    S["schedule<br/>(daily at SCHEDULE)"] --> W["weathy<br/>app/app.py"]
    W -->|"WeatherIL(LOCATION, LANGUAGE)"| IMS["IMS forecast<br/>ims.gov.il"]
    W -->|"apprise.notify()"| A["Apprise"]
    A --> T["Telegram (tgram://)"]
    A --> O["Other Apprise targets"]
```

1. On startup, weathy splits `NOTIFIERS` on whitespace and registers every Apprise URL.
2. The `schedule` library runs the job once a day at `SCHEDULE`, in the container's local time. The loop checks for pending jobs every second.
3. The job calls `WeatherIL(LOCATION, LANGUAGE).get_forecast()` and uses the day at index `1` of the returned list. weatheril returns the days in IMS feed order, and the feed starts with the previous day, so index `1` is today. The screenshot shows a forecast sent on 30/01/2024 for 30/01/2024. If IMS ever stops including the previous day, index `1` would be tomorrow.
4. Only the hourly entries whose time of day is later than the current time are included. For example, a job that runs at 18:00 lists the hours from 19:00 on.
5. The message is sent to all Apprise targets with an empty title. The header and the hour labels are wrapped in `<b>` tags, and `notify()` is called without a `body_format`. Telegram renders them as bold; other targets may show the tags literally.

## Components and frameworks

* [Loguru](https://pypi.org/project/loguru/) for logging.
* [schedule](https://pypi.org/project/schedule/) - Python job scheduling for humans.
* [Apprise](https://pypi.org/project/apprise/) - send a notification to almost all of the most popular notification services.
* [weatheril](https://pypi.org/project/weatheril/) - an unofficial IMS (Israel Meteorological Service) Python API wrapper.

## Requirements

- Docker and Docker Compose (recommended), **or** Python 3.10+ with `pip` to run from source.
- Outbound HTTPS access to `ims.gov.il` and to your notification service.
- At least one Apprise notification URL. For Telegram you need a bot token and the chat ID to send to (see below).
- The container's time zone set to Israel time (`TZ=Asia/Jerusalem`) so the schedule and the hourly filter match local time.

## Create a Telegram bot

Skip this section if you use a different Apprise service.

Open [Telegram](https://web.telegram.org/), and sign in to your account or create a new one.

Enter @BotFather in the search tab and choose this bot. (Official Telegram bots have a blue checkmark next to their name.)

[![@BotFather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@BotFather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@BotFather")

Click "Start" to activate the BotFather bot.

[![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")

In response, you receive a list of commands to manage bots.
Choose or type the `/newbot` command and send it.

[![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")

Choose a name for your bot. Your subscribers will see it in the conversation. Then choose a username for your bot. The bot can be found by its username in searches. The username must be unique and end with the word "bot".

[![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")

After you choose a suitable name, the bot is created. You receive a message with a link to your bot (`t.me/<bot_username>`), the bot's **HTTP API token**, recommendations to set up a profile picture and description, and a list of commands to manage your new bot.

[![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")

### Build the Telegram notifier URL

Apprise's Telegram URL format is `tgram://<bot_token>/<chat_id>`:

- `<bot_token>` is the token BotFather gave you.
- `<chat_id>` is the user, group or channel to send to. Send any message to your bot first (Telegram bots can't start a conversation), then open `https://api.telegram.org/bot<bot_token>/getUpdates` and copy the `chat.id` value. Group IDs are negative numbers. In a group with privacy mode on, the bot only sees commands and mentions, so send `/start@<bot_username>` or mention the bot. For a channel, add the bot as an administrator; channel IDs start with `-100`. See the [Apprise Telegram wiki page](https://github.com/caronc/apprise/wiki/Notify_telegram) for more options.

Example (placeholders only):

```text
tgram://123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/987654321
```

## Installation

weathy is published as a Docker image on Docker Hub: [`techblog/weathy`](https://hub.docker.com/r/techblog/weathy).

| Tag | Platforms |
| --- | --- |
| `latest` | `linux/amd64`, `linux/arm64`, `linux/arm/v7` |
| `0.0.1` | `linux/amd64`, `linux/arm64`, `linux/arm/v7` |

Both tags were pushed in January 2024. There are no GitHub releases or git tags. A GitHub Container Registry workflow exists (see [Development](#development)), but no `ghcr.io/t0mer/weathy` image has been published yet.

### Docker Compose

Create a `docker-compose.yaml`:

```yaml
services:
  weathy:
    image: techblog/weathy:latest
    container_name: weathy
    restart: always
    environment:
      - NOTIFIERS=tgram://<bot_token>/<chat_id>   # One or more Apprise URLs, separated by spaces
      - TZ=Asia/Jerusalem
      - LOCATION=1        # Location ID from the locations table (1 = Jerusalem)
      - LANGUAGE=he       # Hebrew; the message text is Hebrew only
      - SCHEDULE=08:00    # Daily send time, HH:MM (24-hour)
    volumes:
      - "/etc/localtime:/etc/localtime:ro"
```

Then start it:

```bash
docker compose up -d
docker compose logs -f weathy
```

The `docker-compose.yaml` in this repository is the same template with empty values; fill them in before you use it.

### Docker run

```bash
docker run -d \
  --name weathy \
  --restart always \
  -e NOTIFIERS="tgram://<bot_token>/<chat_id>" \
  -e TZ=Asia/Jerusalem \
  -e LOCATION=1 \
  -e LANGUAGE=he \
  -e SCHEDULE=08:00 \
  -v /etc/localtime:/etc/localtime:ro \
  techblog/weathy:latest
```

### From source

```bash
git clone https://github.com/t0mer/weathy.git
cd weathy
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

export NOTIFIERS="tgram://<bot_token>/<chat_id>"
export LOCATION=1
export LANGUAGE=he
export SCHEDULE=08:00
python app/app.py
```

When you run from source, the schedule uses your machine's local time zone. Running from source needs Python 3.10 or newer, because weatheril uses `int | None` type annotations. The published image (January 2024) runs Python 3.12. The current Dockerfile targets `python:3.14-rc-slim-bookworm`, but no image has been published from it yet.

## Configuration

All configuration is done with environment variables. There are no CLI flags or config files.

| Variable | Required | Default (Docker image) | Description |
| --- | --- | --- | --- |
| `NOTIFIERS` | Yes | `""` | One or more [Apprise URLs](#supported-notifications), separated by spaces. If it is empty, the job still runs but nothing is sent. |
| `LOCATION` | Yes | `""` | IMS location ID from the [locations table](#locations-table), for example `1` for Jerusalem. |
| `LANGUAGE` | Yes | `""` | Forecast language passed to weatheril. Use `he`. weatheril also accepts `en`, but weathy's message template and weather-condition names are Hebrew only, so `en` gives a mixed-language message. |
| `SCHEDULE` | Yes | not set | Daily send time in `HH:MM` 24-hour format (for example `07:30` or `20:00`). `HH:MM:SS` also works. |
| `TZ` | Recommended | not set | Container time zone. Set `Asia/Jerusalem` so `SCHEDULE` and the hourly filter use Israel time. Mounting `/etc/localtime` read-only only helps if the host itself is on Israel time, and `TZ` takes precedence over it. |
| `LOG_LEVEL` | No | `DEBUG` | Set in the Dockerfile but not read by the application. |

The Docker image also sets `PYTHONIOENCODING=utf-8` and `LANG=C.UTF-8` so Hebrew text is logged and sent correctly.

### Locations table

The table below lists the location IDs. The authoritative list lives in the weatheril library, which may contain more IDs or slightly different names.

| Id | Location |
| ------------ | ----------- |
| 1| Jerusalem|
| 2| Tel Aviv - Yafo|
| 3| Haifa|
| 4| Rishon le Zion|
| 5| Petah Tiqva|
| 6| Ashdod|
| 7| Netania|
| 8| Beer Sheva|
| 9| Bnei Brak|
| 10| Holon|
| 11| Ramat Gan|
| 12| Asheqelon|
| 13| Rehovot|
| 14| Bat Yam|
| 15| Bet Shemesh|
| 16| Kfar Sava|
| 17| Herzliya|
| 18| Hadera|
| 19| Modiin|
| 20| Ramla|
| 21| Raanana|
| 22| Modiin Illit|
| 23| Rahat|
| 24| Hod Hasharon|
| 25| Givatayim|
| 26| Kiryat Ata|
| 27| Nahariya|
| 28| Beitar Illit|
| 29| Um al-Fahm|
| 30| Kiryat Gat|
| 31| Eilat|
| 32| Rosh Haayin|
| 33| Afula|
| 34| Nes-Ziona|
| 35| Akko|
| 36| Elad|
| 37| Ramat Hasharon|
| 38| Karmiel|
| 39| Yavneh|
| 40| Tiberias|
| 41| Tayibe|
| 42| Kiryat Motzkin|
| 43| Shfaram|
| 44| Nof Hagalil|
| 45| Kiryat Yam|
| 46| Kiryat Bialik|
| 47| Kiryat Ono|
| 48| Maale Adumim|
| 49| Or Yehuda|
| 50| Zefat|
| 51| Netivot|
| 52| Dimona|
| 53| Tamra |
| 54| Sakhnin|
| 55| Yehud|
| 56| Baka al-Gharbiya|
| 57| Ofakim|
| 58| Givat Shmuel|
| 59| Tira|
| 60| Arad|
| 61| Migdal Haemek|
| 62| Sderot|
| 63| Araba|
| 64| Nesher|
| 65| Kiryat Shmona|
| 66| Yokneam Illit|
| 67| Kafr Qassem|
| 68| Kfar Yona|
| 69| Qalansawa|
| 70| Kiryat Malachi|
| 71| Maalot-Tarshiha|
| 72| Tirat Carmel|
| 73| Ariel|
| 74| Or Akiva|
| 75| Bet Shean|
| 76| Mizpe Ramon|
| 77| Lod|
| 78| Nazareth|
| 79| Qazrin|
| 80| En Gedi|
| 200| Nimrod Fortress|
| 201| Banias|
| 202| Tel Dan|
| 203| Snir Stream|
| 204| Horshat Tal |
| 205| Ayun Stream|
| 206| Hula|
| 207| Tel Hazor|
| 208| Akhziv|
| 209| Yehiam Fortress|
| 210| Baram|
| 211| Amud Stream|
| 212| Korazim|
| 213| Kfar Nahum|
| 214| Majrase |
| 215| Meshushim Stream|
| 216| Yehudiya |
| 217| Gamla|
| 218| Kursi |
| 219| Hamat Tiberias|
| 220| Arbel|
| 221| En Afek|
| 222| Tzipori|
| 223| Hai-Bar Carmel|
| 224| Mount Carmel|
| 225| Bet Shearim|
| 226| Mishmar HaCarmel |
| 227| Nahal Me‘arot|
| 228| Dor-HaBonim|
| 229| Tel Megiddo|
| 230| Kokhav HaYarden|
| 231| Maayan Harod|
| 232| Bet Alpha|
| 233| Gan HaShlosha|
| 235| Taninim Stream|
| 236| Caesarea|
| 237| Tel Dor|
| 238| Mikhmoret Sea Turtle|
| 239| Beit Yanai|
| 240| Apollonia|
| 241| Mekorot HaYarkon|
| 242| Palmahim|
| 243| Castel|
| 244| En Hemed|
| 245| City of David|
| 246| Me‘arat Soreq|
| 248| Bet Guvrin|
| 249| Sha’ar HaGai|
| 250| Migdal Tsedek|
| 251| Haniya Spring|
| 252| Sebastia|
| 253| Mount Gerizim|
| 254| Nebi Samuel|
| 255| En Prat|
| 256| En Mabo‘a|
| 257| Qasr al-Yahud|
| 258| Good Samaritan|
| 259| Euthymius Monastery|
| 261| Qumran|
| 262| Enot Tsukim|
| 263| Herodium|
| 264| Tel Hebron|
| 267| Masada |
| 268| Tel Arad|
| 269| Tel Beer Sheva|
| 270| Eshkol|
| 271| Mamshit|
| 272| Shivta|
| 273| Ben-Gurion’s Tomb|
| 274| En Avdat|
| 275| Avdat|
| 277| Hay-Bar Yotvata|
| 278| Coral Beach|

## Usage

1. Set the environment variables and start the container.
2. On startup, the log shows `Setting Apprise notification channels` and one `Adding: ...` line per Apprise URL.
3. Every day at `SCHEDULE`, weathy fetches the forecast and sends it to every Apprise target.

There is no web UI, API, or bot command. To change the location, time, or targets, update the environment variables and recreate the container:

```bash
docker compose up -d --force-recreate
```

To send to several targets at once, separate the URLs with spaces:

```text
NOTIFIERS=tgram://<bot_token>/<chat_id> discord://<webhook_id>/<webhook_token>
```

A sample message looks like this (Hebrew, as shown in the screenshot):

```text
תחזית ארצית ליום שלישי ה 30/01/2024

<IMS national forecast text>
טמפרטורה ממוצעת: 14°-9°

19:00 :12, גשום, 100% סיכוי לגשם
...
```

The weather condition (`גשום` above) can be empty, for example `12, , 100%`. See [Troubleshooting](#troubleshooting).

## Supported notifications

weathy sends through Apprise, so it supports every service Apprise supports. [Check out the Apprise wiki for the full, up-to-date list](https://github.com/caronc/apprise/wiki). For Telegram, use `tgram://<bot_token>/<chat_id>`.

<details>
<summary>Popular notification services (snapshot of the Apprise documentation; the wiki is authoritative)</summary>

The table below shows some of the services Apprise supports and example service URLs. Click any service for details on how to configure it.

| Notification Service | Service ID | Default Port | Example Syntax |
| -------------------- | ---------- | ------------ | -------------- |
| [Apprise API](https://github.com/caronc/apprise/wiki/Notify_apprise_api)  | apprise:// or apprises:// | (TCP) 80 or 443 | apprise://hostname/Token
| [AWS SES](https://github.com/caronc/apprise/wiki/Notify_ses)  | ses://   | (TCP) 443   | ses://user@domain/AccessKeyID/AccessSecretKey/RegionName<br/>ses://user@domain/AccessKeyID/AccessSecretKey/RegionName/email1/email2/emailN
| [Boxcar](https://github.com/caronc/apprise/wiki/Notify_boxcar)  | boxcar://   | (TCP) 443   | boxcar://hostname<br />boxcar://hostname/@tag<br/>boxcar://hostname/device_token<br />boxcar://hostname/device_token1/device_token2/device_tokenN<br />boxcar://hostname/@tag/@tag2/device_token
| [Discord](https://github.com/caronc/apprise/wiki/Notify_discord)  | discord://   | (TCP) 443   | discord://webhook_id/webhook_token<br />discord://avatar@webhook_id/webhook_token
| [Emby](https://github.com/caronc/apprise/wiki/Notify_emby)  | emby:// or embys:// | (TCP) 8096 | emby://user@hostname/<br />emby://user:password@hostname
| [Enigma2](https://github.com/caronc/apprise/wiki/Notify_enigma2)  | enigma2:// or enigma2s:// | (TCP) 80 or 443 | enigma2://hostname
| [Faast](https://github.com/caronc/apprise/wiki/Notify_faast) | faast://    | (TCP) 443    | faast://authorizationtoken
| [FCM](https://github.com/caronc/apprise/wiki/Notify_fcm) | fcm://    | (TCP) 443    | fcm://project@apikey/DEVICE_ID<br />fcm://project@apikey/#TOPIC<br/>fcm://project@apikey/DEVICE_ID1/#topic1/#topic2/DEVICE_ID2/
| [Flock](https://github.com/caronc/apprise/wiki/Notify_flock) | flock://    | (TCP) 443    | flock://token<br/>flock://botname@token<br/>flock://app_token/u:userid<br/>flock://app_token/g:channel_id<br/>flock://app_token/u:userid/g:channel_id
| [Gitter](https://github.com/caronc/apprise/wiki/Notify_gitter) | gitter://    | (TCP) 443    | gitter://token/room<br/>gitter://token/room1/room2/roomN
| [Google Chat](https://github.com/caronc/apprise/wiki/Notify_googlechat) | gchat://    | (TCP) 443    | gchat://workspace/key/token
| [Gotify](https://github.com/caronc/apprise/wiki/Notify_gotify) | gotify:// or gotifys://   | (TCP) 80 or 443    | gotify://hostname/token<br />gotifys://hostname/token?priority=high
| [Growl](https://github.com/caronc/apprise/wiki/Notify_growl)  | growl://   | (UDP) 23053   | growl://hostname<br />growl://hostname:portno<br />growl://password@hostname<br />growl://password@hostname:port</br>**Note**: you can also use the get parameter _version_ which can allow the growl request to behave using the older v1.x protocol. An example would look like: growl://hostname?version=1
| [Home Assistant](https://github.com/caronc/apprise/wiki/Notify_homeassistant)       | hassio:// or hassios://   | (TCP) 8123 or 443 | hassio://hostname/accesstoken<br />hassio://user@hostname/accesstoken<br />hassio://user:password@hostname:port/accesstoken<br />hassio://hostname/optional/path/accesstoken
| [IFTTT](https://github.com/caronc/apprise/wiki/Notify_ifttt) | ifttt://    | (TCP) 443    | ifttt://webhooksID/Event<br />ifttt://webhooksID/Event1/Event2/EventN<br/>ifttt://webhooksID/Event1/?+Key=Value<br/>ifttt://webhooksID/Event1/?-Key=value1
| [Join](https://github.com/caronc/apprise/wiki/Notify_join) | join://   | (TCP) 443    | join://apikey/device<br />join://apikey/device1/device2/deviceN/<br />join://apikey/group<br />join://apikey/groupA/groupB/groupN<br />join://apikey/DeviceA/groupA/groupN/DeviceN/
| [KODI](https://github.com/caronc/apprise/wiki/Notify_kodi) | kodi:// or kodis://    | (TCP) 8080 or 443   | kodi://hostname<br />kodi://user@hostname<br />kodi://user:password@hostname:port
| [Kumulos](https://github.com/caronc/apprise/wiki/Notify_kumulos) | kumulos:// | (TCP) 443 | kumulos://apikey/serverkey
| [LaMetric Time](https://github.com/caronc/apprise/wiki/Notify_lametric) | lametric:// | (TCP) 443 | lametric://apikey@device_ipaddr<br/>lametric://apikey@hostname:port<br/>lametric://client_id@client_secret
| [Mailgun](https://github.com/caronc/apprise/wiki/Notify_mailgun) | mailgun:// | (TCP) 443 | mailgun://user@hostname/apikey<br />mailgun://user@hostname/apikey/email<br />mailgun://user@hostname/apikey/email1/email2/emailN<br />mailgun://user@hostname/apikey/?name="From%20User"
| [Matrix](https://github.com/caronc/apprise/wiki/Notify_matrix) | matrix:// or matrixs://  | (TCP) 80 or 443 | matrix://hostname<br />matrix://user@hostname<br />matrixs://user:pass@hostname:port/#room_alias<br />matrixs://user:pass@hostname:port/!room_id<br />matrixs://user:pass@hostname:port/#room_alias/!room_id/#room2<br />matrixs://token@hostname:port/?webhook=matrix<br />matrix://user:token@hostname/?webhook=slack&format=markdown
| [Mattermost](https://github.com/caronc/apprise/wiki/Notify_mattermost) | mmost:// or mmosts:// | (TCP) 8065 | mmost://hostname/authkey<br />mmost://hostname:80/authkey<br />mmost://user@hostname:80/authkey<br />mmost://hostname/authkey?channel=channel<br />mmosts://hostname/authkey<br />mmosts://user@hostname/authkey<br />
| [Microsoft Teams](https://github.com/caronc/apprise/wiki/Notify_msteams) | msteams://  | (TCP) 443   | msteams://TokenA/TokenB/TokenC/
| [MQTT](https://github.com/caronc/apprise/wiki/Notify_mqtt) | mqtt://  or mqtts:// | (TCP) 1883 or 8883   | mqtt://hostname/topic<br />mqtt://user@hostname/topic<br />mqtts://user:pass@hostname:9883/topic
| [Nextcloud](https://github.com/caronc/apprise/wiki/Notify_nextcloud) | ncloud:// or nclouds:// | (TCP) 80 or 443 | ncloud://adminuser:pass@host/User<br/>nclouds://adminuser:pass@host/User1/User2/UserN
| [NextcloudTalk](https://github.com/caronc/apprise/wiki/Notify_nextcloudtalk) | nctalk:// or nctalks:// | (TCP) 80 or 443 | nctalk://user:pass@host/RoomId<br/>nctalks://user:pass@host/RoomId1/RoomId2/RoomIdN
| [Notica](https://github.com/caronc/apprise/wiki/Notify_notica) | notica://  | (TCP) 443   | notica://Token/
| [Notifico](https://github.com/caronc/apprise/wiki/Notify_notifico) | notifico://  | (TCP) 443   | notifico://ProjectID/MessageHook/
| [Office 365](https://github.com/caronc/apprise/wiki/Notify_office365) | o365://  | (TCP) 443   | o365://TenantID:AccountEmail/ClientID/ClientSecret<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail1/TargetEmail2/TargetEmailN
| [OneSignal](https://github.com/caronc/apprise/wiki/Notify_onesignal) | onesignal:// | (TCP) 443 | onesignal://AppID@APIKey/PlayerID<br/>onesignal://TemplateID:AppID@APIKey/UserID<br/>onesignal://AppID@APIKey/#IncludeSegment<br/>onesignal://AppID@APIKey/Email
| [Opsgenie](https://github.com/caronc/apprise/wiki/Notify_opsgenie) | opsgenie:// | (TCP) 443 | opsgenie://APIKey<br/>opsgenie://APIKey/UserID<br/>opsgenie://APIKey/#Team<br/>opsgenie://APIKey/\*Schedule<br/>opsgenie://APIKey/^Escalation
| [ParsePlatform](https://github.com/caronc/apprise/wiki/Notify_parseplatform) | parsep:// or parseps:// | (TCP) 80 or 443 | parsep://AppID:MasterKey@Hostname<br/>parseps://AppID:MasterKey@Hostname
| [PopcornNotify](https://github.com/caronc/apprise/wiki/Notify_popcornnotify) | popcorn://  | (TCP) 443   | popcorn://ApiKey/ToPhoneNo<br/>popcorn://ApiKey/ToPhoneNo1/ToPhoneNo2/ToPhoneNoN/<br/>popcorn://ApiKey/ToEmail<br/>popcorn://ApiKey/ToEmail1/ToEmail2/ToEmailN/<br/>popcorn://ApiKey/ToPhoneNo1/ToEmail1/ToPhoneNoN/ToEmailN
| [Prowl](https://github.com/caronc/apprise/wiki/Notify_prowl) | prowl://   | (TCP) 443    | prowl://apikey<br />prowl://apikey/providerkey
| [PushBullet](https://github.com/caronc/apprise/wiki/Notify_pushbullet) | pbul://    | (TCP) 443    | pbul://accesstoken<br />pbul://accesstoken/#channel<br/>pbul://accesstoken/A_DEVICE_ID<br />pbul://accesstoken/email@address.com<br />pbul://accesstoken/#channel/#channel2/email@address.net/DEVICE
| [Pushjet](https://github.com/caronc/apprise/wiki/Notify_pushjet) | pjet:// or pjets:// | (TCP) 80 or 443 | pjet://hostname/secret<br />pjet://hostname:port/secret<br />pjets://secret@hostname/secret<br />pjets://hostname:port/secret
| [Push (Techulus)](https://github.com/caronc/apprise/wiki/Notify_techulus) | push://    | (TCP) 443    | push://apikey/
| [Pushed](https://github.com/caronc/apprise/wiki/Notify_pushed) | pushed://    | (TCP) 443    | pushed://appkey/appsecret/<br/>pushed://appkey/appsecret/#ChannelAlias<br/>pushed://appkey/appsecret/#ChannelAlias1/#ChannelAlias2/#ChannelAliasN<br/>pushed://appkey/appsecret/@UserPushedID<br/>pushed://appkey/appsecret/@UserPushedID1/@UserPushedID2/@UserPushedIDN
| [Pushover](https://github.com/caronc/apprise/wiki/Notify_pushover)  | pover://   | (TCP) 443   | pover://user@token<br />pover://user@token/DEVICE<br />pover://user@token/DEVICE1/DEVICE2/DEVICEN<br />**Note**: you must specify both your user_id and token
| [PushSafer](https://github.com/caronc/apprise/wiki/Notify_pushsafer)  | psafer:// or psafers://  | (TCP) 80 or 443  | psafer://privatekey<br />psafers://privatekey/DEVICE<br />psafer://privatekey/DEVICE1/DEVICE2/DEVICEN
| [Reddit](https://github.com/caronc/apprise/wiki/Notify_reddit) | reddit:// | (TCP) 443   | reddit://user:password@app_id/app_secret/subreddit<br />reddit://user:password@app_id/app_secret/sub1/sub2/subN
| [Rocket.Chat](https://github.com/caronc/apprise/wiki/Notify_rocketchat) | rocket:// or rockets://  | (TCP) 80 or 443   | rocket://user:password@hostname/RoomID/Channel<br />rockets://user:password@hostname:443/#Channel1/#Channel1/RoomID<br />rocket://user:password@hostname/#Channel<br />rocket://webhook@hostname<br />rockets://webhook@hostname/@User/#Channel
| [Ryver](https://github.com/caronc/apprise/wiki/Notify_ryver) | ryver://  | (TCP) 443   | ryver://Organization/Token<br />ryver://botname@Organization/Token
| [SendGrid](https://github.com/caronc/apprise/wiki/Notify_sendgrid) | sendgrid://  | (TCP) 443   | sendgrid://APIToken:FromEmail/<br />sendgrid://APIToken:FromEmail/ToEmail<br />sendgrid://APIToken:FromEmail/ToEmail1/ToEmail2/ToEmailN/
| [ServerChan](https://github.com/caronc/apprise/wiki/Notify_serverchan) | serverchan://   | (TCP) 443    | serverchan://token/
| [SimplePush](https://github.com/caronc/apprise/wiki/Notify_simplepush) | spush://   | (TCP) 443    | spush://apikey<br />spush://salt:password@apikey<br />spush://apikey?event=Apprise
| [Slack](https://github.com/caronc/apprise/wiki/Notify_slack) | slack://  | (TCP) 443   | slack://TokenA/TokenB/TokenC/<br />slack://TokenA/TokenB/TokenC/Channel<br />slack://botname@TokenA/TokenB/TokenC/Channel<br />slack://user@TokenA/TokenB/TokenC/Channel1/Channel2/ChannelN
| [SMTP2Go](https://github.com/caronc/apprise/wiki/Notify_smtp2go) | smtp2go:// | (TCP) 443 | smtp2go://user@hostname/apikey<br />smtp2go://user@hostname/apikey/email<br />smtp2go://user@hostname/apikey/email1/email2/emailN<br />smtp2go://user@hostname/apikey/?name="From%20User"
| [Streamlabs](https://github.com/caronc/apprise/wiki/Notify_streamlabs) | strmlabs:// | (TCP) 443 | strmlabs://AccessToken/<br/>strmlabs://AccessToken/?name=name&identifier=identifier&amount=0&currency=USD
| [SparkPost](https://github.com/caronc/apprise/wiki/Notify_sparkpost) | sparkpost:// | (TCP) 443 | sparkpost://user@hostname/apikey<br />sparkpost://user@hostname/apikey/email<br />sparkpost://user@hostname/apikey/email1/email2/emailN<br />sparkpost://user@hostname/apikey/?name="From%20User"
| [Spontit](https://github.com/caronc/apprise/wiki/Notify_spontit) | spontit://  | (TCP) 443   | spontit://UserID@APIKey/<br />spontit://UserID@APIKey/Channel<br />spontit://UserID@APIKey/Channel1/Channel2/ChannelN
| [Syslog](https://github.com/caronc/apprise/wiki/Notify_syslog) | syslog://  | (UDP) 514 (_if hostname specified_) | syslog://<br />syslog://Facility<br />syslog://hostname<br />syslog://hostname/Facility
| [Telegram](https://github.com/caronc/apprise/wiki/Notify_telegram) | tgram://  | (TCP) 443   | tgram://bottoken/ChatID<br />tgram://bottoken/ChatID1/ChatID2/ChatIDN
| [Twitter](https://github.com/caronc/apprise/wiki/Notify_twitter) | twitter://  | (TCP) 443   | twitter://CKey/CSecret/AKey/ASecret<br/>twitter://user@CKey/CSecret/AKey/ASecret<br/>twitter://CKey/CSecret/AKey/ASecret/User1/User2/User2<br/>twitter://CKey/CSecret/AKey/ASecret?mode=tweet
| [Twist](https://github.com/caronc/apprise/wiki/Notify_twist) | twist://  | (TCP) 443   | twist://password:login<br/>twist://password:login/#channel<br/>twist://password:login/#team:channel<br/>twist://password:login/#team:channel1/channel2/#team3:channel
| [XBMC](https://github.com/caronc/apprise/wiki/Notify_xbmc) | xbmc:// or xbmcs://    | (TCP) 8080 or 443   | xbmc://hostname<br />xbmc://user@hostname<br />xbmc://user:password@hostname:port
| [XMPP](https://github.com/caronc/apprise/wiki/Notify_xmpp) | xmpp:// or xmpps://    | (TCP) 5222 or 5223   | xmpp://user:password@hostname<br />xmpps://user:password@hostname:port?jid=user@hostname/resource<br/>xmpps://user:password@hostname/target@myhost, target2@myhost/resource
| [Webex Teams (Cisco)](https://github.com/caronc/apprise/wiki/Notify_wxteams) | wxteams://  | (TCP) 443   | wxteams://Token
| [Zulip Chat](https://github.com/caronc/apprise/wiki/Notify_zulip) | zulip://  | (TCP) 443   | zulip://botname@Organization/Token<br />zulip://botname@Organization/Token/Stream<br />zulip://botname@Organization/Token/Email

</details>

## Troubleshooting

- **The container exits right after it starts.** `SCHEDULE` or `NOTIFIERS` is missing or invalid. `SCHEDULE` must be set and use `HH:MM` (24-hour). Running from source without `NOTIFIERS` exported also fails at startup. Check `docker logs weathy`.
- **Nothing is sent, and there are no errors.** `NOTIFIERS` is empty, or the Apprise URL is wrong. Check the `Adding: ...` lines in the log and test the URL with the [Apprise CLI](https://github.com/caronc/apprise/wiki/CLI_Usage).
- **You receive `aw snap something went wrong`.** Fetching or parsing the IMS forecast failed. The log contains the exception after `aw snap something went wrong:`. Common causes: an empty or invalid `LOCATION`, an empty `LANGUAGE`, no network access to `ims.gov.il`, or a change in the IMS data format.
- **The message arrives at the wrong time.** The schedule uses the container's local time. Set `TZ=Asia/Jerusalem`. The `/etc/localtime` mount only helps if the host is on Israel time, and `TZ` takes precedence.
- **The hourly list is short or empty.** Only hours later than the current time of day are listed, so a late schedule time shows fewer hours.
- **The weather condition is empty (for example `12, , 100%`).** This is a known limitation. `app.py` looks up the condition with `HE_WEATHER_CODES.get(str(code))`. Since weatheril 0.35.0 (April 2025) that table's keys are integers, so the lookup always fails on a source install or a newly built image. The published image (built with weatheril 0.32.0) still shows conditions, but codes missing from the table are empty there too; the screenshot shows `12, , 100%` at 19:00.
- **Other targets show `<b>` tags literally.** The message uses `<b>` tags and is sent without a `body_format`. Telegram renders them as bold; other Apprise targets may not.
- **The weather conditions are in Hebrew even with `LANGUAGE=en`.** This is expected: the message template is Hebrew only.

## Security notes

- The Apprise URLs in `NOTIFIERS` contain credentials (for example, your Telegram bot token). Treat them as secrets: don't commit them to git or paste them in issues, and prefer an `.env` file or your orchestrator's secret store.
- If a bot token leaks, revoke it with @BotFather (`/revoke`) and update `NOTIFIERS`.
- weathy opens no ports and accepts no incoming connections. It only makes outbound HTTPS requests to the IMS and your notification services.

## Development

Project layout:

```text
app/app.py              # the whole application: config, IMS fetch, message formatting, scheduling
requirements.txt        # Python dependencies (unpinned, plus security floors from Snyk)
Dockerfile              # python:3.14-rc-slim-bookworm based image
docker-compose.yaml     # compose template
VERSION                 # image version used by the Docker Hub workflow
screenshots/            # README images
.github/workflows/      # CI
```

GitHub Actions workflows:

| Workflow | File | Trigger | Publishes |
| --- | --- | --- | --- |
| Docker Build | `docker-image.yml` | Manual (`workflow_dispatch`), or after a "Create Release" workflow completes | `techblog/weathy:latest` and `techblog/weathy:<VERSION>` to Docker Hub, for `linux/amd64`, `linux/arm64` and `linux/arm/v7` |
| Publish to GHCR | `publish-ghcr.yml` | Manual (`workflow_dispatch`) with an optional `tag` input (default `latest`) | `ghcr.io/t0mer/weathy:<tag>` and `ghcr.io/t0mer/weathy:latest`, for the same three platforms |

The repository has no "Create Release" workflow, so in practice the Docker Hub build runs only when started manually.

Build the image locally:

```bash
docker build -t weathy:dev .
```

There are no tests or linters in the repository.

## Contributing

Issues and pull requests are welcome at [github.com/t0mer/weathy](https://github.com/t0mer/weathy). Please keep changes focused, describe how you tested them, and never include real bot tokens or chat IDs.

## License

This repository has no license file.
