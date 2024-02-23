##
# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/
##

import json
import math
import smtplib
import sys
import os
from datetime import datetime, timedelta
from email.message import EmailMessage

with open('pihole_configs.json', 'r') as file:
    config = json.load(file)

##
# Converts seconds to days, hours, minutes, and seconds.
#  Args:
#    seconds: The number of seconds to convert.
#  Returns:
#    A tuple containing the number of days, hours, minutes, and seconds.
##
def seconds_to_dhms(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    formatted_time = f"{days} days {hours} hours {minutes} minutes {seconds} seconds"
    return formatted_time

def convert_size(size_bits):
   if size_bits == 0:
       return "0 Bps"
   size_name = ("Kbps", "Mbps", "Gbps", "Tbps", "Pbps")
   i = int(math.floor(math.log(size_bits, 1000000)))
   p = math.pow(1000000, i)
   s = round(size_bits / p, 2)
   return "%s %s" % (s, size_name[i])

##
# 1. Get server uptime from the '/proc/uptime' file
# 2. Two values are returned, so assign them to unique variables
# 3. Use the 'seconds_to_dhms' function to output human readable uptime and
#    assign them to the 'uptime_string' variable
##
with open("/proc/uptime", "r") as uptime_file:
    uptime_data = uptime_file.read().strip().split()
total_uptime = float(uptime_data[0])
idle_time = float(uptime_data[1])
uptime_string=seconds_to_dhms(total_uptime)

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
Uptime:
{uptime_string}
Download Speed: {dl_speed_mb}
Upload Speed: {ul_speed_mb}
""".format(uptime_string=uptime_string,dl_speed_mb=dl_speed_mb,ul_speed_mb=ul_speed_mb)
msg.set_content(body)

##
# Set sender and recipient
##
msg['From'] = from_email_addr
msg['To'] = to_email_addr

##
# Set your email subject
##
msg['Subject'] = 'Updating and rebooting...'

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
