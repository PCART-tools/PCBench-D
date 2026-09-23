def _handle_exception(result):
    if isinstance(result, RemoteException):
        raise result.exception_type(result.msg.encode("utf-8").decode("unicode_escape"))
