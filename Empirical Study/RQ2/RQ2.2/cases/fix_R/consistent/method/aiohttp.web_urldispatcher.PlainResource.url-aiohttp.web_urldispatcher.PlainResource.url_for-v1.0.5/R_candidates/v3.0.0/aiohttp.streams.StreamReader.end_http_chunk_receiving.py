    def end_http_chunk_receiving(self):
        if self._http_chunk_splits is None:
            raise RuntimeError("Called end_chunk_receiving without calling "
                               "begin_chunk_receiving first")
        if not self._http_chunk_splits or \
                self._http_chunk_splits[-1] != self.total_bytes:
            self._http_chunk_splits.append(self.total_bytes)
