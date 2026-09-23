    def close(self):
        """
        Finalize this object, making the underlying file a complete
        PDF file.
        """
        if self._file is not None:
            self._file.finalize()
            self._file.close()
            self._file = None
        elif self._keep_empty:  # True *or* UNSET.
            _api.warn_deprecated("3.8", message=(
                "Keeping empty pdf files is deprecated since %(since)s and support "
                "will be removed %(removal)s."))
            PdfFile(self._filename, metadata=self._metadata).close()  # touch the file.
