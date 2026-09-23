    def begin_http_chunk_receiving(self):
        if self._http_chunk_splits is None:
            self._http_chunk_splits = []
