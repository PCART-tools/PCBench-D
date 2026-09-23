    def _serialize_io(self, obj):
        while True:
            chunk = obj.read(self._chunk_size)
            if not chunk:
                break
            if isinstance(chunk, str):
                yield from self._serialize_str(chunk)
            else:
                yield from self._serialize_bytes(chunk)
