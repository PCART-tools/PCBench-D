def _handle_exception(result):
    if isinstance(result, RemoteException):
        exception_msg = result.msg.encode("utf-8").decode("unicode_escape")
        # We wrap exception re-creation here in case some exception classes
        # cannot be constructed directly from a string.
        exc = None
        try:
            exc = result.exception_type(exception_msg)
        except BaseException as e:
            raise RuntimeError(  # noqa: B904
                f"Failed to create original exception type. Error msg was {str(e)}"
                f" Original exception on remote side was {exception_msg}"
            ) from e

        if exc is not None:
            raise exc
