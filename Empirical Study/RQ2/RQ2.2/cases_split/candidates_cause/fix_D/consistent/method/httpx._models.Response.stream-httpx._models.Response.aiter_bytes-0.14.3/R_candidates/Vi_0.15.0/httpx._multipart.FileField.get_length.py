    def get_length(self) -> int:
        headers = self.render_headers()

        if isinstance(self.file, (str, bytes)):
            return len(headers) + len(self.file)

        # Let's do our best not to read `file` into memory.
        try:
            file_length = peek_filelike_length(self.file)
        except OSError:
            # As a last resort, read file and cache contents for later.
            assert not hasattr(self, "_data")
            self._data = to_bytes(self.file.read())
            file_length = len(self._data)

        return len(headers) + file_length
