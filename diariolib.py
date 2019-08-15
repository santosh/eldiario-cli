import uuid
import requests


class ElDiario(object):
    def __init__(self, *args, **kwargs):
        super(ElDiario, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def new_entry(self):
        # self.args is tuple of len == 1
        # 1st index of tuple is Namespace object
        current_time = self.args[-1].new

        # make a POST request to : /api/entry

    def delete_entry(self, id):
        pass
        # Make a DELETE Request to /api/entry/{id}

    def list_entry(self):
        pass
        # Make a GET Request to /api/entries

    def edit_entry(self, id, data):
        pass
        # Make a PUT Request to /api/entry/{id}

    def get_single_entry(self):
        """Get's a single JSON. Useful when verbosely listing many """
        pass
        # Make a GEt Request to /api/entry/{id}

    def get_new_uuid(self):
        return str(uuid.uuid4())
