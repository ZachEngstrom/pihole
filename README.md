```
 ____ ___ _   _  ___  _     _____
|  _ \_ _| | | |/ _ \| |   | ____|
| |_) | || |_| | | | | |   |  _|
|  __/| ||  _  | |_| | |___| |___
|_|  |___|_| |_|\___/|_____|_____|
```

## Overview

This repository provides scripts and configuration files to automate [PiHole](https://docs.pi-hole.net/) updates, email notifications, and more, keeping your network secure and ad-free with minimal manual intervention.

### Key Features

- Automated Updates:
   - Refreshes package lists
   - Installs upgrades
   - Removes unused dependencies
   - Updates Pi-hole itself
   - Updates gravity lists
   - Restarts Raspberry Pi
- Informative Email Notifications:
   - Pre-update email with uptime information (potentially additional metrics to be added)
   - Post-update email with uptime information (potentially additional metrics to be added)
- Comprehensive Documentation:
   - Clear setup instructions with links to external resources
   - Helpful tips for SSH access, file transfer, and log monitoring

## Prerequisites

- Active Pi-hole installation
   - Consider using the instructional written by [CrossTalk Solutions](https://www.crosstalksolutions.com/the-worlds-greatest-pi-hole-and-unbound-tutorial-2023/) for the initial setup. The [YouTube video](https://youtu.be/cE21YjuaB6o) worked well for me.
- Basic knowledge of Linux terminal commands

## Getting Started

1. Clone this repository to your Raspberry Pi or server.
   - Github: `git clone https://github.com/ZachEngstrom/pihole.git`
   - Gitlab: `git clone https://gitlab.com/engza/pihole.git`
1. Install [Speedtest CLI](https://github.com/sivel/speedtest-cli)
   - run `pip install speedtest-cli`
1. Follow the instructions below

#### Send an Email using Python

1. Run this command in the root of your Raspberry Pi or server:<br>`cp pihole/{pihole_configs.example.json,pihole_email_before_restart.py,pihole_email_after_restart.py} ./ && mv pihole_configs.example.json pihole_configs.json`
1. Create a new email account and an email app password by following these instructions: [Send an Email using Python](./docs/smtp.md). You can stop when you get to "The Email-Sending Script".
1. Edit the configs file - `sudo nano pihole_configs.json`
   1. Use your arrow keys to navigate to the 3 values, remove the `REPLACE_WITH_THE_...` text and then fill in the appropriate values.
   1. You created the `from_addr` and `from_pass` values when you followed the [Send an Email using Python](./docs/smtp.md) document.
   1. For the `to_addr` value, I get the email message as a text to my phone. Here are some examples of how to do with with major cellular providers. Remember to replace "REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER" with your cell phone number:
      - **AT&T**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@txt.att.net
      - **Verizon**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@vtext.com
      - **T-Mobile**: REPLACE_WITH_YOUR_TEN_DIGIT_PHONE_NUMBER@tmomail.net
      - [notepage.net/smtp.htm](https://www.notepage.net/smtp.htm)
      - [avtech.com/articles/138/list-of-email-to-sms-addresses](https://avtech.com/articles/138/list-of-email-to-sms-addresses/)
   1. Once you have all 3 values filled in, you can press <kbd>[^X]</kbd>, <kbd>[y]</kbd> and <kbd>[return]</kbd> to save your changes and exit the file.
1. Test that the email files work by running<br>`python pihole_email_before_restart.py "$(cat /proc/uptime)" "$(speedtest-cli --csv)"`<br>and<br>`python pihole_email_after_restart.py "$(cat /proc/uptime)" "$(speedtest-cli --csv)"`<br>in your terminal and then either checking your inbox or watching your phone for a text (depending on the value you entered for the `to_addr`).

#### Update Script Using Bash

1. Run `cp pihole/pihole_update.sh pihole_update.sh`
1. Run `sudo chmod +x ./pihole_update.sh` to make the file executable.

You can now run this script any time by running `./pihole_update.sh` in your terminal.

#### Automatically Update and Send Emails Using Cron

1. Run `crontab -e` in your terminal
1. Add the following code to the end of the file:<br><pre>55 1 * * 6 python pihole\_email\_before\_restart.py "$(cat /proc/uptime)" "$(speedtest-cli --csv)"
0 2 * * 6 ./pihole_update.sh >> pihole.log 2>&1
30 2 * * 6 python pihole\_email\_after\_restart.py "$(cat /proc/uptime)" "$(speedtest-cli --csv)"</pre>
   - The 1st line runs `pihole_email_before_restart.py` every Saturday at 1:55 AM.
   - The 2nd line runs `pihole_update.sh` every Saturday at 2:00 AM and captures the output in the `pihole.log` file (it will automatically get created if it's not already there).
   - The 3rd line runs `pihole_email_after_restart.py` every Saturday at 2:30 AM.
1. Now press <kbd>[^X]</kbd>, <kbd>[y]</kbd> and <kbd>[return]</kbd> to save your changes and exit the file.
1. Validate that the file saved by running `crontab -l` in your terminal. You should see the lines that you added.

## Helpful

- SSH into your Rasberry Pi
   - `ssh PI_USER_NAME@PI_IP_ADDRESS`
- Copy files from your local machine to your Raspberry Pi via SSH
   - `scp pihole_update.sh pihole_email_before_restart.py pihole_email_after_restart.py pihole_configs.example.json PI_USER_NAME@PI_IP_ADDRESS:~`
- Copy files from your Raspberry Pi to your local machine via SSH
   - `scp PI_USER_NAME@PI_IP_ADDRESS:pihole.log ./`
- Watch the `pihole.log` in real time as the update script is running (typically used when manually intiating the update script)
   - `tail -f pihole.log`
- Use [crontab.guru](https://crontab.guru/) if you'd like to adjust when your cron jobs run.

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

## To Do / Consideration

- [ ] Set the email app password as an [environment variable](https://networkdirection.net/python/resources/env-variable/) instead of in the config file.
- [ ] Email python files don't have a fall back for null/empty values. This should be addressed.

## Contributions and Feedback

All contributions and suggestions are welcome! Please create an issue or pull request on GitHub or Gitlab.