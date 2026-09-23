    def iter_raw(self) -> typing.Iterator[bytes]:
        """
        A byte-iterator over the raw response content.
        """
        if self.is_stream_consumed:
            raise StreamConsumed()
        if self.is_closed:
            raise ResponseClosed()

        self.is_stream_consumed = True
        with map_exceptions(HTTPCORE_EXC_MAP, request=self._request):
            for part in self._raw_stream:
                yield part
        self.close()
