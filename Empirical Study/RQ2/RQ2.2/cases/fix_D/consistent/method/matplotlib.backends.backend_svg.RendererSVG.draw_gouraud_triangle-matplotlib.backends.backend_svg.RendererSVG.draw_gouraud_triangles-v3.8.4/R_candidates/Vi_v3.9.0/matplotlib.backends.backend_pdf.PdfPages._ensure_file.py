    def _ensure_file(self):
        if self._file is None:
            self._file = PdfFile(self._filename, metadata=self._metadata)  # init.
        return self._file
