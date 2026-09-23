    def render_data(self) -> typing.Iterator[bytes]:
        if isinstance(self.file, (str, bytes)):
            yield to_bytes(self.file)
            return

        if hasattr(self, "_data"):
            # Already rendered.
            yield self._data
            return

        if self._consumed:  # pragma: nocover
            self.file.seek(0)
        self._consumed = True

        for chunk in self.file:
            yield to_bytes(chunk)
