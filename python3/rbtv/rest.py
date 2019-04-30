
from datetime import datetime,timedelta

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import requests
import json


token = '*** REMOVED ***'
class API:
    def __init__(self):
        self.headers = {'Authorization': 'Bearer ' + token}
        self.notifications = []
        self.ws = None

    def _handleMessage(self, ws, msg):
        prefix = '42'
        print("WS: ", msg[0])
        if msg[0] == 'AC_AUTHENTICATION_REQ':
            resp = prefix + str(['CA_AUTHENTICATION', {'appName':'rbtv-page', 'token':token}]).replace("'",'"').replace(' ','')
            print("WS-SEND: ", resp)
            ws.send(resp)
        
        elif msg[0] == 'AC_AUTHENTICATION_RESULT':
            print("Auth: ", msg[1])
            if msg[1]['result'] == False:
                ws.close()
        
        elif msg[0] == 'AC_PING':
            resp = prefix + str(['CA_PONG', msg[1]]).replace("'",'"').replace(' ','')
            print("WS-SEND: ", resp)
            ws.send(resp)
        
        elif msg[0] == 'AC_NOTIFICATION':
            self.notifications.append(msg[1])
        
    def reloadNotifications(self):
        self.notifications = []

        if self.ws:
            self.ws.close()

        def on_message(ws, message):
            if message.startswith('42'):
                msg = json.loads(message[2:])
                self._handleMessage(ws, msg)

        def on_error(ws, error):
            print("WS_ERR: ", error)

        def on_close(ws):
            print("### closed ###")

        def on_open(ws):
            print("### opend ###")

        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://api.rocketbeans.tv/socket.io/?EIO=3&transport=websocket",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
        self.ws.on_open = on_open
        def run(*args):
            self.ws.run_forever()

        thread.start_new_thread(run, ())
    
    def getNotifications(self):
        return self.notifications

    def getSelf(self):
        req = 'https://api.rocketbeans.tv/v1/user/self'
        print(req)
        r = requests.get(req, headers = self.headers)
        data = json.loads(r.text)
        print(data['success'])
        if data['success']:
            return data
        else:
            return None

    def getSchedule(self, today: datetime):
        print(today)

        yesterday = today + timedelta(days = -1)
        tomorrow = today + timedelta(days = 2)

        withouttime = datetime(yesterday.year, yesterday.month, yesterday.day)
        timestamp = datetime.timestamp(withouttime)
        withouttime = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        timestamp2 = datetime.timestamp(withouttime)

        print(int(timestamp), int(timestamp2))

        req = 'https://api.rocketbeans.tv/v1/schedule/normalized?startDay=' +str(int(timestamp))+ '&endDay=' +str(int(timestamp2))
        print(req)
        r = requests.get(req, headers = self.headers)
        data = json.loads(r.text)
        print(data['success'])
        return data

    def getStreamCount(self):
        req = 'https://api.rocketbeans.tv/StreamCount'
        print(req)
        r = requests.get(req, headers = self.headers)
        data = json.loads(r.text)
        print(data['success'])
        return data

    def getBlogPromo(self):
        req = 'https://api.rocketbeans.tv/v1/blog/promo/all?offset=0&limit=2'
        print(req)
        r = requests.get(req, headers = self.headers)
        data = json.loads(r.text)
        print(data['success'])
        return data
