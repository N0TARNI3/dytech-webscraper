import requests
from datetime import date, timedelta
import numpy as np
import re
import os
import shutil

# Main download link of the required files
DOMAIN = 'https://links.sgx.com/1.0.0/derivatives-historical/'

# Compute for the unique ID and the most recent market day
START_DATE= '2022-11-29'
RECENT_DATE= date.today() - timedelta(days=1)
while RECENT_DATE.weekday() > 4:
    RECENT_DATE-= timedelta(days=1)
ID = np.busday_count(START_DATE, RECENT_DATE)

# List of files that needs to be downloaded
FILES = [
    'WEBPXTICK_DT.zip',
    'TickData_structure.dat',
    'TC.txt',
    'TC_structure.dat'
]

def GET_FILES(id):
    # Create new directory where files will be saved
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(dir_path + "/FILES", str(RECENT_DATE))
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    # Download needed files thru requests
    for file in FILES:
        response = requests.get(DOMAIN + '53' + str(id) + '/' + file)
        d = response.headers.get('content-disposition')
        filename = re.findall('filename=(.+)', d)[0]
        file = os.path.join(folder, filename)
        with open(file, 'wb') as f:
            f.write(response.content)    


GET_ALL_FILES = int(input('\nWhat files do you want to scrape? \n0 - Today\'s files only \n1 - Including Historical Files \n>> '))

if GET_ALL_FILES == 1:
    for i in range(4):
        GET_FILES(ID)
        ID -= 1
        RECENT_DATE-= timedelta(days=1)        
        while RECENT_DATE.weekday() > 4:
            RECENT_DATE-= timedelta(days=1)
elif GET_ALL_FILES == 0:
    GET_FILES(ID)
else:
    print('Invalid input. Please try again.')
