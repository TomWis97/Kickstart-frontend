#!/usr/bin/env python3
import urllib.request
import re
import random
import ssl
# Get download page.
isoType = 'DVD ISO'
regexString = r'(?<=href=").+?(?=">{})'.format(isoType)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
downloadPage = urllib.request.urlopen(
    'https://www.centos.org/download/', context=ctx).read().decode('UTF-8')
mirrorListUrl = re.search(regexString, downloadPage).group(0)
# Get mirror list.
page = urllib.request.urlopen(mirrorListUrl).read().decode('UTF-8')
splitPage = page.split('<br><br>')
validSections = []
for i in splitPage:
    if i.startswith("<a href"):
        validSections.append(i)
correctSection = validSections[0]
# Remove the random newlines.
urlsString = ''.join(line.strip() for line in correctSection)
urlsList = re.findall(r"(?<=href=').+?(?=')", urlsString)
try:
    returnUrl = random.choice(urlsList)
except:
    # Docker hub does not seem to like random numbers.
    # So we just fix it this way:
    returnUrl = urlsList[3] # Chosen by a faire dice roll.
    # Guaranteed to be random.
    # https://xkcd.com/221/
print(returnUrl)
