class HttpException(Exception):

    code = None
    headers = ()
    message = ''
