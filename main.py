import requests
from datetime import date
import numpy as np
import re
import os


# Main download link of the required files
DOMAIN = 'https://links.sgx.com/1.0.0/derivatives-historical/'

# Compute for the unique ID
DATE_START= '2022-11-29'
DATE_TODAY = date.today()
ID = np.busday_count(DATE_START, DATE_TODAY) - 2

# List of files that needs to be downloaded
FILES = [
    'WEBPXTICK_DT.zip',
    'TickData_structure.dat',
    'TC.txt',
    'TC_structure.dat'
]
  
# Create new directory where files will be saved
dir_path = os.path.dirname(os.path.realpath(__file__))
folder = os.path.join(dir_path + "/FILES", str(DATE_TODAY))
os.mkdir(folder)

# Download needed files thru requests
for file in FILES:
    response = requests.get(DOMAIN + '53' + str(ID) + '/' + file)
    d = response.headers.get('content-disposition')
    filename = re.findall('filename=(.+)', d)[0]
    file = os.path.join(folder, filename)
    with open(file, 'wb') as f:
        f.write(response.content)    