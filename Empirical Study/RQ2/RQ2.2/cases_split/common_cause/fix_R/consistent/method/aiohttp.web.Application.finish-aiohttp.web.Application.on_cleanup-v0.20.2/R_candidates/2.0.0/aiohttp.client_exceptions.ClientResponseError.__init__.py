    def __init__(self, *, code=None, message='', headers=None):
        if code is not None:
            self.code = code
            self.message = message
            self.headers = headers

        super().__init__("%s, message='%s'" % (self.code, message))
