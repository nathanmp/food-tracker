import fitbit
import requests
from datetime import date
import os
class FitbitClient:
    def __init__(self):
        try:
            f = open('fitbit.config', 'r')
        except:
            self.enabled = False
            return
            
        self.enabled = True
        fr = f.read()
        f.close()
        frn = fr.split("\n")
        d = {}
        for l in frn:
            if ' = ' not in l:
                continue
            d[l.split(" = ")[0]] = l.split(' = ')[1]
        self.keys = d

    def return_client(self):

        def refreshcb(tok):
            f = open("fitbit.config", "w")
            f.write("consumer_key = " + self.keys['consumer_key'])
            f.write('consumer_secret = ' + self.keys['consumer_secret'])
            f.write('access_token = ' + tok['access_token'])
            f.write('refresh_token = ' + tok['refresh_token'])
            f.write('expires_at = ' + str(tok['expires_at']))
            f.close()

        client = fitbit.Fitbit(self.keys['consumer_key'], self.keys['consumer_secret'],
            access_token=self.keys["access_token"], refresh_token=self.keys['refresh_token'],
            expires_at=float(self.keys['expires_at']), refresh_cb = refreshcb)
        return client

        
    def make_client(self):
        if not self.enabled:
            self.client = False
        return self.return_client()


    def log_food(self, json):
        if self.client == False:
            return -1
        else:
            return self.client.log_food(json)
