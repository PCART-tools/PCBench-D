    async def __aexit__(self, exc_type, exc, tb):
        # We're basing behavior on the exception as it can be caused by
        # user code unrelated to the status of the connection.  If you
        # would like to close a connection you must do that
        # explicitly.  Otherwise connection error handling should kick in
        # and close/recycle the connection as required.
        self._resp.release()
