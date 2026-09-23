    def __init__(self, *, code=None, message='', headers=None):
        if code is not None:
            self.code = code
        self.headers = headers
        self.message = message

        super().__init__("%s, message='%s'" % (self.code, message))
