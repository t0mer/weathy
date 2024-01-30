# weathy
wathy is a python powered bot for sending weather forecast on a scheduled time.

![wathy](screenshots/wathy.png)

## Features
- Send daily weather forecast


## Components and Frameworks used in weathy:
* [Loguru](https://pypi.org/project/loguru/) For logging.
* [schedule](https://pypi.org/project/schedule/) Python job scheduling for humans.
* [apprise](https://pypi.org/project/apprise/) Apprise allows you to send a notification to almost all of the most popular notification services available.
* [weatheril](https://pypi.org/project/weatheril/) weatheril is an unofficial IMS (Israel Meteorological Service) python API wrapper.



## Installation

Before we can start working with weathy, we need to create a new telegram bot. 

### Create Telegram bot
How to Create a New Bot for Telegram
Open [Telegram messenger](https://web.telegram.org/), sign in to your account or create a new one.

 Enter @Botfather in the search tab and choose this bot (Official Telegram bots have a blue checkmark beside their name.)

[![@Botfather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")

Click “Start” to activate BotFather bot.

[![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@start")

In response, you receive a list of commands to manage bots.
Choose or type the /newbot command and send it.

[![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")


Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”

[![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")


After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.

[![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")


weathy is a docker based application that can be installed using docker compose:

```yaml
version: "3.7"

services:

  weathy:
    image: techblog/weathy:latest
    container_name: weathy
    restart: always
    environment:
      - NOTIFIERS= #Apprise notifiers
      - TZ=Asia/Jerusalem
      - LOCATION= # The Location ID of your city.
      - LANGUAGE=he #Currently the only supported language. english will be added soon.
      - SCHEDULE= #Time of the day to send the notification, 80:00, 12:00, 20:00, etc.
    volumes:
      - "/etc/localtime:/etc/localtime:ro"
```

### Environment
* NOTIFIERS: Apprise notifiers
* LOCATION: The Location ID of your city from the attached table.
* LANGUAGE: The forecast language.
* SCHEDULE: Time of the day to send the notification, 80:00, 12:00, 20:00, etc.



### Locations table

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



## Supported Notifications
The section identifies all of the services supported by this library. [Check out the wiki for more information on the supported modules here](https://github.com/caronc/apprise/wiki).

### Popular Notification Services
The table below identifies the services this tool supports and some example service urls you need to use in order to take advantage of it. Click on any of the services listed below to get more details on how you can configure Apprise to access them.

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
| [Twist](https://github.com/caronc/apprise/wiki/Notify_twist) | twist://  | (TCP) 443   | twist://pasword:login<br/>twist://password:login/#channel<br/>twist://password:login/#team:channel<br/>twist://password:login/#team:channel1/channel2/#team3:channel
| [XBMC](https://github.com/caronc/apprise/wiki/Notify_xbmc) | xbmc:// or xbmcs://    | (TCP) 8080 or 443   | xbmc://hostname<br />xbmc://user@hostname<br />xbmc://user:password@hostname:port
| [XMPP](https://github.com/caronc/apprise/wiki/Notify_xmpp) | xmpp:// or xmpps://    | (TCP) 5222 or 5223   | xmpp://user:password@hostname<br />xmpps://user:password@hostname:port?jid=user@hostname/resource<br/>xmpps://user:password@hostname/target@myhost, target2@myhost/resource
| [Webex Teams (Cisco)](https://github.com/caronc/apprise/wiki/Notify_wxteams) | wxteams://  | (TCP) 443   | wxteams://Token
| [Zulip Chat](https://github.com/caronc/apprise/wiki/Notify_zulip) | zulip://  | (TCP) 443   | zulip://botname@Organization/Token<br />zulip://botname@Organization/Token/Stream<br />zulip://botname@Organization/Token/Email
