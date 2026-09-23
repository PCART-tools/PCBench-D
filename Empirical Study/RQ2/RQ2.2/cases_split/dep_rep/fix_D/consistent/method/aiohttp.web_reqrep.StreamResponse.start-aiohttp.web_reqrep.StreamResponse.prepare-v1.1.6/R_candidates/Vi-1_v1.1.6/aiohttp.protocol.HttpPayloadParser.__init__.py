    def __init__(self, message, length=None, compression=True,
                 readall=False, response_with_body=True):
        self.message = message
        self.length = length
        self.compression = compression
        self.readall = readall
        self.response_with_body = response_with_body
