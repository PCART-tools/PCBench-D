def log_response(message, *args, response=None, request=None, logger=request_logger, level=None, exc_info=None):
    """
    Log errors based on HttpResponse status.

    Log 5xx responses as errors and 4xx responses as warnings (unless a level
    is given as a keyword argument). The HttpResponse status_code and the
    request are passed to the logger's extra parameter.
    """
    # Check if the response has already been logged. Multiple requests to log
    # the same response can be received in some cases, e.g., when the
    # response is the result of an exception and is logged at the time the
    # exception is caught so that the exc_info can be recorded.
    if getattr(response, '_has_been_logged', False):
        return

    if level is None:
        if response.status_code >= 500:
            level = 'error'
        elif response.status_code >= 400:
            level = 'warning'
        else:
            level = 'info'

    getattr(logger, level)(
        message, *args,
        extra={
            'status_code': response.status_code,
            'request': request,
        },
        exc_info=exc_info,
    )
    response._has_been_logged = True
