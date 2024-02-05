#!/bin/bash

datetime=$(date +"%Y-%m-%d %T")
printf "\n\n[%s] INFO: pihole_update.sh initiated\n\n" "${datetime}"

datetime=$(date +"%Y-%m-%d %T")
printf "[%s] INFO: running 'sudo apt update'\n" "${datetime}"
sudo apt update

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo apt list --upgradeable'\n" "${datetime}"
sudo apt list --upgradeable

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo apt upgrade -y'\n" "${datetime}"
sudo apt upgrade -y

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo apt autoremove'\n" "${datetime}"
sudo apt autoremove

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo pihole -up'\n\n" "${datetime}"
sudo pihole -up

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo pihole -g'\n\n" "${datetime}"
sudo pihole -g

datetime=$(date +"%Y-%m-%d %T")
printf "\n[%s] INFO: running 'sudo reboot'\n\n" "${datetime}"
printf "[%s] INFO: pihole_update.sh finished\n\n" "${datetime}"
printf "********************************************************************************\n\n"
sudo reboot
