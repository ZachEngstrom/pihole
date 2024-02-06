```
 ____ ___ _   _  ___  _     _____
|  _ \_ _| | | |/ _ \| |   | ____|
| |_) | || |_| | | | | |   |  _|
|  __/| ||  _  | |_| | |___| |___
|_|  |___|_| |_|\___/|_____|_____|
```

## Description

This repository assumes that you have [PiHole](https://docs.pi-hole.net/) up and running. Consider using the instructional written by [CrossTalk Solutions](https://www.crosstalksolutions.com/the-worlds-greatest-pi-hole-and-unbound-tutorial-2023/) for the initial setup. The [YouTube video](https://youtu.be/cE21YjuaB6o) worked well for me.

## Ad Lists

As recommended in the [CrossTalk Solutions](https://www.crosstalksolutions.com/the-worlds-greatest-pi-hole-and-unbound-tutorial-2023/) tutorial, I referenced [The Firebog](https://firebog.net/) for a majority of the lists that I implemented.

Here is a complete list of the ad lists that I've implemented:
- <https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts>
- <https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt>
- <https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts>
- <https://adaway.org/hosts.txt>
- <https://v.firebog.net/hosts/AdguardDNS.txt>
- <https://v.firebog.net/hosts/Easyprivacy.txt>
- <https://v.firebog.net/hosts/Prigent-Ads.txt>
- <https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareHosts.txt>
- <https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt>
- <https://zerodot1.gitlab.io/CoinBlockerLists/hosts_browser>

I did have to whitelist `slackb.com` to use slack on my network.

## Automation

Here are the steps that I took to make my PiHole self-sufficient.

### Send an Email using Python

1. Read through the entire [Send an Email using Python](./docs/smtp.md) document and then go back and follow the instructions up until "The Email-Sending Script".
1. Copy these 3 files to the root of your Raspberry Pi or server:
   - [pihole\_configs.example.json](./pihole_configs.example.json)
   - [pihole\_email\_before\_restart.py](./pihole_email_before_restart.py)
   - [pihole\_email\_after\_restart.py](./pihole_email_after_restart.py)
1. Set the configs file by running `mv pihole_configs.example.json pihole_configs.json` in your terminal and then `sudo nano pihole_configs.json`.
1. Use your arrow keys to navigate to the values, remove the `REPLACE_WITH_THE_...` text and then fill in the appropriate values.
1. You created the `from_addr` and `from_pass` when you followed the [Send an Email using Python](./docs/smtp.md) document.
1. For the `to_addr`, I get the email message as a text to my phone. Here are some examples of how to do with with major cellular providers. Remember to replace "REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER" with your cell phone number:
   - **AT&T**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@txt.att.net
   - **Verizon**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@vtext.com
   - **T-Mobile**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@tmomail.net
   - [notepage.net/smtp.htm](https://www.notepage.net/smtp.htm)
   - [avtech.com/articles/138/list-of-email-to-sms-addresses](https://avtech.com/articles/138/list-of-email-to-sms-addresses/)
1. Once you have all 3 values filled in, you can press <kbd>[^X]</kbd>, <kbd>[y]</kbd> and <kbd>[return]</kbd> to save your changes and exit the file.
1. Test that the email files work by running `python pihole_email_before_restart.py` and `python pihole_email_after_restart.py` in your terminal and then either checking your inbox or watching your phone for a text (depending on the value you entered for the `to_addr`).

### Update Script Using Bash

1. Copy the [pihole_update.sh](./pihole_update.sh) file to the root of your Raspberry Pi or server. No editing necessary.
1. Run `sudo chmod +x ./pihole_update.sh` to make the file executable.

You can now run this script any time by running `./pihole_update.sh` in your terminal.

### Automatically Update and Send Emails Using Cron

1. Run `sudo crontab -e` in your terminal
1. Add the following code to the end of the file:<br><pre>55 1 * * 6 python pihole\_email\_before\_restart.py
0 2 * * 6 ./pihole_update.sh >> pihole.log 2>&1
30 2 * * 6 python pihole\_email\_after\_restart.py</pre>
   - The 1st line is saying to run the *pihole_email_before_restart.py* file every Saturday morning at 1:55AM.
   - The 2nd line is saying to run the *pihole_update.sh* file every Saturday morning at 2:00AM and capture the output in the *pihole.log* file (it will automatically get created if it's not already there).
   - The 3rd line is saying to run the `pihole_email_after_restart.py` file every Saturday morning at 2:30AM.
   - Use [crontab.guru](https://crontab.guru/) if you'd like to adjust when these scripts run.
1. Now press <kbd>[^X]</kbd>, <kbd>[y]</kbd> and <kbd>[return]</kbd> to save your changes and exit the file.
1. Validate that the file saved by running `sudo crontab -l` in your terminal. You should see the values that you entered

## Helpful

- SSH into your Rasberry Pi
   - `ssh PI_USER_NAME@PI_IP_ADDRESS`
- Copy files from your local machine to your Raspberry Pi via SSH
   - `scp pihole_update.sh pihole_email_before_restart.py pihole_email_after_restart.py pihole_configs.example.json PI_USER_NAME@PI_IP_ADDRESS:~`
- Copy files from your Raspberry Pi to your local machine via SSH
   - `scp PI_USER_NAME@PI_IP_ADDRESS:pihole.log ./`
- Watch the *pihole.log* in real time as the update script is running (typically used when manually intiating the update script)
   - `tail -f pihole.log`

## To Do / Consideration

- Set the email pass as an environment variable instead of in the config file - [Python Environment Variables](https://networkdirection.net/python/resources/env-variable/)