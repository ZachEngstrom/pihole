##
# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/
##

import json
import math
import smtplib
import sys
from datetime import datetime, timedelta
from email.message import EmailMessage

with open('pihole_configs.json', 'r') as file:
    config = json.load(file)

def get_time(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1,1,1) + sec
    return "%d days %d hours %d minutes %d seconds" % (d.day-1, d.hour, d.minute, d.second)

def convert_size(size_bits):
   if size_bits == 0:
       return "0 Bps"
   size_name = ("Kbps", "Mbps", "Gbps", "Tbps", "Pbps")
   i = int(math.floor(math.log(size_bits, 1000000)))
   p = math.pow(1000000, i)
   s = round(size_bits / p, 2)
   return "%s %s" % (s, size_name[i])

##
# Get uptime using `cat /proc/uptime`
##
proc_uptime = sys.argv[1]
uptime_seconds = proc_uptime.split(' ',1)[0]
uptime_formatted = get_time(float(uptime_seconds))

##
# Get speedtest results using `speedtest-cli --csv`
##
speedtest_full = sys.argv[2]
speedtest_split = speedtest_full.split(',')
dl_speed_mb = convert_size(float(speedtest_split[6]))
ul_speed_mb = convert_size(float(speedtest_split[7]))

##
# Set the sender email and password and recipient email
##
from_email_addr = config['email']['from_addr']
from_email_pass = config['email']['from_pass']
to_email_addr = config['email']['to_addr']

##
# Create a message object
##
msg = EmailMessage()

##
# Set the email body
##
body = """
Uptime: {uptime_formatted}
Download Speed: {dl_speed_mb}
Upload Speed: {ul_speed_mb}
""".format(uptime_formatted=uptime_formatted,dl_speed_mb=dl_speed_mb,ul_speed_mb=ul_speed_mb)
msg.set_content(body)

##
# Set sender and recipient
##
msg['From'] = from_email_addr
msg['To'] = to_email_addr

##
# Set your email subject
##
msg['Subject'] = 'Updated and rebooted'

##
# Connecting to server and sending email
# Edit the following line with your provider's SMTP server details
##
server = smtplib.SMTP('smtp.gmail.com', 587)

##
# Comment out the next line if your email provider doesn't use TLS
##
server.starttls()

##
# Login to the SMTP server
##
server.login(from_email_addr, from_email_pass)

##
# Send the message
##
server.send_message(msg)
print('Email sent')

##
# Disconnect from the Server
##
server.quit()
