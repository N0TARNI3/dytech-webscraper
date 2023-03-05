import requests
from datetime import date
import numpy as np

# Main download link of the required files
DOMAIN = 'https://links.sgx.com/1.0.0/derivatives-historical/'

DATE_START= '2022-11-29'
DATE_TODAY = date.today()
ID = np.busday_count(DATE_START, DATE_TODAY) - 2

class FILESTRUCT:
  def __init__(self, url, type):
    self.url = url
    self.type = type

FILES = []
FILES.append(FILESTRUCT('53' + str(ID) + '/WEBPXTICK_DT-' + DATE_TODAY.strftime('%Y%m%d') + '.zip', '.zip'))

response = requests.get(DOMAIN+FILES[0].url)
with open("WEBPXTICK_DT"+DATE_TODAY.strftime('%Y%m%d')+'.zip', 'wb') as file:
    file.write(response.content)    