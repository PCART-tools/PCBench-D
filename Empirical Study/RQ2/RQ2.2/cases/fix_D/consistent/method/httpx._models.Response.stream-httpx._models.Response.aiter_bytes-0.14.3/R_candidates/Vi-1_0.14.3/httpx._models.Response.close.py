    def close(self) -> None:
        """
        Close the response and release the connection.
        Automatically called if the response body is read to completion.
        """
        if not self.is_closed:
            self.is_closed = True
            if self._request is not None:
                self._elapsed = self.request.timer.elapsed
            self._raw_stream.close()
