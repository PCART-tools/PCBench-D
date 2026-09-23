    def close(self):
        """
        Finalize this object, making the underlying file a complete
        PDF file.
        """
        self._file.finalize()
        self._file.close()
        if (self.get_pagecount() == 0 and not self.keep_empty and
                not self._file.passed_in_file_object):
            os.remove(self._file.fh.name)
        self._file = None
