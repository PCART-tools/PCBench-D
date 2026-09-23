class HttpException(http.client.HTTPException):

    code = None
    headers = ()
    message = ''
