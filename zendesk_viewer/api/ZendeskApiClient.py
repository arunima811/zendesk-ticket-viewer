import os

import requests


class ZendeskApiClient:
    def __init__(self):
        self.base_url = "https://zccintern22.zendesk.com/api/v2/"
        self.next = self.base_url + "tickets.json?page[size]=25"
        self.prev = None
        self.username = os.environ.get('ZENDESK_USERNAME')
        self.password = os.environ.get('ZENDESK_PASSWORD')

    def _fetch(self, url):
        try:
            resp = requests.get(url, auth=(self.username, self.password))
            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except Exception as e:
            return None

    def get_user(self):
        self_url = self.base_url + "users/me"
        if self.username and self.password:
            resp = self._fetch(self_url)
            if resp and resp['user']['id']:
                return resp['user']['name']
        return None

    def reset(self):
        self.next = self.base_url + "tickets.json?page[size]=25"
        self.prev = None

    def has_next(self):
        return True if self.next is not None else False
    
    def has_prev(self):
        return True if self.prev is not None else False

    def get_tickets(self, direction='next'):
        if direction == 'next':
            if self.next:
                resp = self._fetch(self.next)
                self.next = resp['links']['next']
                self.prev = resp['links']['prev']

                self.next = resp['links']['next'] if resp['meta']['has_more'] else None
                self.prev = resp['links']['prev']

                return resp['tickets']
            else:
                return None
        elif direction == 'prev':
            if self.prev:
                resp = self._fetch(self.prev)
                self.next = resp['links']['next']
                self.prev = resp['links']['prev']

                self.next = resp['links']['next'] if resp['meta']['has_more'] else None
                self.prev = resp['links']['prev']

                return resp['tickets']
            else:
                return None
