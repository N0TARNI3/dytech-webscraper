import requests
from datetime import date, timedelta
import numpy as np
import re
import os
import shutil
import logging

# Logging configurations
logs = logging.getLogger(__name__)
logs.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream_format = logging.Formatter('%(asctime)s | %(levelname)8s | %(message)s', datefmt='%H:%M:%S')
stream.setFormatter(stream_format)
logs.addHandler(stream)
logging.basicConfig(filename="scraper.log", level=logging.DEBUG, format='%(asctime)s | %(levelname)8s | %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

# Main download link of the required files
DOMAIN = 'https://links.sgx.com/1.0.0/derivatives-historical/'

# List of files that needs to be downloaded
FILES = [
    'WEBPXTICK_DT.zip',
    'TickData_structure.dat',
    'TC.txt',
    'TC_structure.dat'
]

def GET_FILES(id,date):
    logs.info(f"Getting files from {date.strftime('%m-%d-%Y')}")

    # Create new directory where files will be saved
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(f"{dir_path}\FILES", str(date))
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    # Download needed files thru requests
    for file in FILES:
        run = 1
        while(run == 1): # Loop for retry prompts
            logs.info(f"Fetching: {file}")
            try:
                response = requests.get(f"{DOMAIN}53{id}1/{file}")

                # Error handling
                if "/CustomErrorPage.aspx" in response.url:
                    raise Exception(f"File {file} from {date} was not found...")
                if response.status_code != 200:
                    raise Exception(f"{response.status_code}:{response.reason}")

                d = response.headers.get('content-disposition')
                filename = re.findall('filename=(.+)', d)[0]
                file = os.path.join(folder, filename)

                try:
                    with open(file, 'wb') as f:
                        f.write(response.content)            
                        logs.info(f"{filename} successfully downloaded!")
                except Exception as e:
                    logs.error(e)
                    
            except Exception as e:
                logs.error(e)
                print("\nCheck if your system has the correct date, or you have stable internet connection.\nDo you want to retry, or proceed to the next file?")
                run = int(input("0 - Proceed | 1 - Retry \n>> "))

def main():
    # Compute for the unique ID and the most recent SGX market day
    START_DATE= '2022-11-29'
    RECENT_DATE= date.today() - timedelta(days=1)
    while RECENT_DATE.weekday() > 4:
        RECENT_DATE-= timedelta(days=1)
    ID = np.busday_count(START_DATE, RECENT_DATE)

    GET_ALL_FILES = int(input('\nWhat files do you want to scrape? \n0 - Today\'s files only \n1 - Including Historical Files \n>> '))

    if GET_ALL_FILES == 1:
        for i in range(4):
            GET_FILES(ID,RECENT_DATE)
            ID -= 1
            RECENT_DATE-= timedelta(days=1)        
            while RECENT_DATE.weekday() > 4:
                RECENT_DATE-= timedelta(days=1)
    elif GET_ALL_FILES == 0:
        GET_FILES(ID,RECENT_DATE)
    else:
        print('Invalid input. Please try again.')

if __name__ == '__main__':
    main()