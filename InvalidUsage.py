#/usr/bin/env python3

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


    def to_dict(self):
        rv = dict()
        sub = dict()
        rv['_status'] = "ERR"

        sub['code'] = self.status_code
        sub['message'] = self.message

        rv['_error'] = sub
        return rv


