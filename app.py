import requests
import pandas as pd
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv
import os

####################################################################
# Disabling Cert Verify 
import ssl

from tgfeed import TGFeeds
ssl._create_default_https_context = ssl._create_unverified_context
####################################################################

def sebi_results_page_response():
  
  url = "https://www.sebi.gov.in/sebiweb/ajax/department/getresultinfo.jsp"

  payload = 'nextValue=1&next=s&search=&year=2024&type=1&doDirect=1'
  headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en-IN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.sebi.gov.in'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return response


def latest_published_results(results_resp):

  df = pd.read_html(StringIO(results_resp.text))
  print(df)
  data_list = df[0].values.tolist()
  page_date= data_list[0][0]
  info = data_list[0][1]

  page_date = datetime.strptime(page_date, "%b %d, %Y").date()
  now = datetime.now().date()
  if(now <= page_date):
    return (info,page_date)
  else:
    return (None,None)

if __name__ == "__main__":
    load_dotenv()
    
    results_resp = sebi_results_page_response()
    info,page_date = latest_published_results(results_resp=results_resp)
    if info and page_date is not None:
      channel_id = "@sebiinfobot"
      tgf = TGFeeds(channel_id=channel_id,bot_token=os.environ.get('TG_BOT_TOKEN'))
      entry = {
        "info" : info,
        "page_date" : page_date,
        "image_url" : "https://img2.rojgarlive.com/careers/2024/07/sebi-result-2024-to-be-released-at-sebigovin-download-the-result-for-the-officer-29-ju-66a7644d02dba89379310-1200.webp"
      }
      tgf.post_image_message(entry)