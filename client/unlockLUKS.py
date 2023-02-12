#!/usr/bin/python

import requests
import subprocess
import StringIO

URL='https://api-host/path/to/your/api'
DUOUSER='user@yourdomain'
KEYNAME='key-name'
LUKSDEVS=['dev1', 'dev2']

r = requests.post(URL, json={'user': DUOUSER, 'key': KEYNAME})
data = r.json()

if data['result'] == 'allow':
    for dev in LUKSDEVS:
        subprocess.Popen(['/sbin/cryptsetup', 'open', '--type', 'luks', '-d', '-', '/dev/systemvg/' + dev, dev], stdin=subprocess.PIPE).communicate(data['key'])
        subprocess.call(['/bin/mount', '/dev/mapper/' + dev])

