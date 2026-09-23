class HttpErrorException(HttpException):

    def __init__(self, code, message='', headers=None):
        self.code = code
        self.headers = headers
        self.message = message
