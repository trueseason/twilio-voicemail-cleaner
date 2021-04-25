import datetime
import requests
import base64
from enum import Enum

class DateFilter(Enum):
    EXACT_DATE_ONLY = 1
    INCLUDE_EARLIER_DATES = 2
    INCLUDE_LATER_DATES = 3

class Voicemail:
    root_url = 'https://api.twilio.com'
    pageSize = 100

    def __init__(self, account_id, auth_token):
        self.twilio_base_url = f'{self.root_url}/2010-04-01/Accounts/{account_id}'
        self.twilio_session = requests.Session()
        self.twilio_session.auth = (account_id, auth_token)

    def list_voicemails(self, url):
        return self.http_get(url)

    def list_voicemails_by_date(self, date_created, filter=DateFilter.EXACT_DATE_ONLY):
        date_filter = "=" if filter is DateFilter.EXACT_DATE_ONLY else "<=" if filter is DateFilter.INCLUDE_EARLIER_DATES else ">="
        date_created = date_created if filter is not DateFilter.INCLUDE_EARLIER_DATES else date_created + datetime.timedelta(days=1)
        url = f'{self.twilio_base_url}/Recordings.json?PageSize={self.pageSize}&DateCreated{date_filter}{date_created.strftime("%Y-%m-%d")}'
        return self.http_get(url)

    def delete_voicemails_by_date(self, date_created, filter=DateFilter.EXACT_DATE_ONLY, recordLimit=10000):
        res = self.list_voicemails_by_date(date_created, filter)
        while True:
            for vm in res["recordings"]:
                self.http_delete(f'{self.root_url}/{vm["uri"]}')
            if not res["next_page_uri"] or res["end"] >= recordLimit:
                return res["end"] if res["end"] == 0 else res["end"]+1
            res = self.list_voicemails(
                url=f'{self.root_url}/{res["next_page_uri"]}')

    def http_get(self, url):
        res = self.twilio_session.get(url)
        res.raise_for_status()
        return res.json()

    def http_post(self, url, data={}):
        res = self.twilio_session.post(url, data=data)
        res.raise_for_status()
        return res.json()

    def http_delete(self, url):
        res = self.twilio_session.delete(url)
        res.raise_for_status()
        return res.json()
