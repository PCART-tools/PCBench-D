    def __init__(self, request_info, history, *,
                 code=0, message='', headers=None):
        self.request_info = request_info
        self.code = code
        self.message = message
        self.headers = headers
        self.history = history

        super().__init__("%s, message='%s'" % (code, message))
