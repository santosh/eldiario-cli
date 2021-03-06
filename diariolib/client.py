import datetime
import getpass
import logging
import os
import json
import uuid

import requests

try:
    import httplib
except:
    import http.client as httplib

from diariolib import formatter
from diariolib import editor

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.expanduser("~")+"/eldiario.log",
    format="%(asctime)s:%(levelname)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %Z",
)

class ElDiario(object):
    user = getpass.getuser()
    def __init__(self, *args, **kwargs):
        super(ElDiario, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def backend_running(self):
        # Check if configured mongo server can be reached.
        conn = httplib.HTTPConnection("localhost:8080", timeout=1)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False

    def new_entry(self, current_time):
        header = {"Content-Type": "application/json"}
        payload = {
            "id": self.get_new_uuid(),
            "body": editor.Editor().get_text_from_new(),
            "created": current_time,
            "modified": current_time,
            "author": self.user,
        }
        r = requests.post('http://localhost:8080/entry',
                        headers=header,
                        data=json.dumps(payload))

        logging.info("new entry received: %s" % r.text)

    def delete_entry(self, _ids):
        # Make a DELETE Request to /api/entry/{id}

        for _id in _ids:
            requests.delete(f'http://localhost:8080/entry/{_id}')


    def list_entry(self):
        # Make a GET Request to /api/entries
        header = {"Content-Type": "application/json"}
        
        r = requests.get('http://localhost:8080/entry',
                        headers=header)

        formatter.json_to_row(r.text)

    def update_entry(self, entry_id):
        # Make a PUT Request to entry/{id}
        header = {"Content-Type": "application/json"}
        
        r = requests.get(f'http://localhost:8080/entry/{entry_id}', headers=header)
        # FIXME: r.text should not newlines but concrete JSON data
        
        strdict = r.text.replace("\n", "")
        dic = dict(eval(strdict))
        
        payload = {
            "id": entry_id,
            "body": editor.Editor().editor_from_message(dic["created"], dic["body"]),
            "created": dic["created"],
            "modified": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "author": self.user,
        }
        r = requests.put(f'http://localhost:8080/entry/{entry_id}',
                        headers=header,
                        data=json.dumps(payload))

    def get_single_entry(self, entry_id):
        """Get's a single JSON. Useful when verbosely listing many """
        # Make a GEt Request to /api/entry/{id}
        header = {"Content-Type": "application/json"}

        url = 'http://localhost:8080/entry{}'.format(str(entry_id))

        r = requests.post(url, headers=header)

        logging.info(r.text)


    def get_new_uuid(self):
        return uuid.uuid4().hex[:8]
