class HttpMethodNotAllowed(HttpException):

    code = 405
    message = 'Method Not Allowed'
