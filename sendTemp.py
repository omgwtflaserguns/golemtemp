#!/usr/bin/python

import requests
import logging
from subprocess import Popen, PIPE

logging.basicConfig(filename='golemtemp.log', level=logging.INFO)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

DEBUG = 1

urlpattern = 'http://www.golem.de/projekte/ot/temp.php?dbg={}&token=3812c58726f0d9489fdf42ac3b208653&city=N%%C3%%BCrnberg&zip=90402&token=3812c58726f0d9489fdf42ac3b208653&lat=49.453089&long=11.048217&type=other&temp={}'
temp_raw = run_cmd("cat /sys/bus/w1/devices/28-000007b38daf/w1_slave")
temp_raw = temp_raw.split('\n')[1][29:32]
temp = "{}.{}".format(temp_raw[:2], temp_raw[-1])
url = urlpattern.format(DEBUG, temp)
response = requests.post(url)

if response.status_code == 200:
    logging.info('Temperaturübermittlung erfolgreich: {}'.format(temp))
else:
    logging.error('Temperaturübermittlung fehlgeschlagen: {}'.format(temp))





