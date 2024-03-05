#!/bin/bash

datetime() {
  date +"%Y-%m-%d %T"
}

printf "\n\n[%s] INFO: pihole_update.sh initiated\n\n" "$(datetime)"

printf "[%s] INFO: running 'sudo apt update'\n" "$(datetime)"
sudo apt update

printf "\n[%s] INFO: running 'sudo apt list --upgradeable'\n" "$(datetime)"
sudo apt list --upgradeable

printf "\n[%s] INFO: running 'sudo apt upgrade -y'\n" "$(datetime)"
sudo apt upgrade -y

printf "\n[%s] INFO: running 'sudo apt autoremove -y'\n" "$(datetime)"
sudo apt autoremove -y

printf "\n[%s] INFO: running 'sudo pihole -up'\n\n" "$(datetime)"
sudo pihole -up

printf "\n[%s] INFO: running 'sudo pihole -g'\n\n" "$(datetime)"
sudo pihole -g

printf "\n[%s] INFO: pihole update finished\n\n" "$(datetime)"

printf "[%s] INFO: running 'sudo service cron restart'\n\n" "$(datetime)"
sudo service cron restart

printf "[%s] INFO: formatting pihole.log file\n\n" "$(datetime)"
# Remove "WARNING: apt does not have a stable CLI interface. Use with caution in scripts."
sed -i '/apt does not have a stable/d' pihole.log
# Remove empty lines
sed -i '/^$/d' pihole.log
# Insert empty line before pattern match for "***"
sed -i '/\*\*\*/i \

' pihole.log
# Insert empty line after pattern match for "***"
sed -i '/\*\*\*/a\

' pihole.log

printf "[%s] INFO: running 'sudo reboot'\n\n" "$(datetime)"
printf "********************************************************************************\n\n"
sudo reboot
