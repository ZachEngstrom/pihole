# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/

import smtplib
import json
from email.message import EmailMessage

with open('pihole_configs.json', 'r') as file:
    config = json.load(file)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#Set the sender email and password and recipient emaiç
from_email_addr = config['email']['from_addr']
from_email_pass = config['email']['from_pass']
to_email_addr = config['email']['to_addr']

# Create a message object
msg = EmailMessage()

# Set the email body
body = "PiHole uptime: "+str(display_time(get_uptime(),3))
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set your email subject
msg['Subject'] = 'Updated and rebooted'

# Connecting to server and sending email
# Edit the following line with your provider's SMTP server details
server = smtplib.SMTP('smtp.gmail.com', 587)

# Comment out the next line if your email provider doesn't use TLS
server.starttls()
# Login to the SMTP server
server.login(from_email_addr, from_email_pass)

# Send the message
server.send_message(msg)

print('Email sent')

#Disconnect from the Server
server.quit()
