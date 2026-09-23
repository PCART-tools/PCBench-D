    @asyncio.coroutine
    def readchunk(self):
        """Returns a tuple of (data, end_of_http_chunk). When chunked transfer
        encoding is used, end_of_http_chunk is a boolean indicating if the end
        of the data corresponds to the end of a HTTP chunk , otherwise it is
        always False.
        """
        if self._exception is not None:
            raise self._exception

        if not self._buffer and not self._eof:
            if (self._http_chunk_splits and
                    self._cursor == self._http_chunk_splits[0]):
                # end of http chunk without available data
                self._http_chunk_splits = self._http_chunk_splits[1:]
                return (b"", True)
            yield from self._wait('readchunk')

        if not self._buffer:
            # end of file
            return (b"", False)
        elif self._http_chunk_splits is not None:
            while self._http_chunk_splits:
                pos = self._http_chunk_splits[0]
                self._http_chunk_splits = self._http_chunk_splits[1:]
                if pos > self._cursor:
                    return (self._read_nowait(pos-self._cursor), True)
            return (self._read_nowait(-1), False)
        else:
            return (self._read_nowait_chunk(-1), False)
