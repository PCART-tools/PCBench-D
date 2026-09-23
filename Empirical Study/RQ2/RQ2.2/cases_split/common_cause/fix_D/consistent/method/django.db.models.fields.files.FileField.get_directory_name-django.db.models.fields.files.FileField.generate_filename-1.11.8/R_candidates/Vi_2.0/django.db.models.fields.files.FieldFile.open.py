    def open(self, mode='rb'):
        self._require_file()
        if hasattr(self, '_file') and self._file is not None:
            self.file.open(mode)
        else:
            self.file = self.storage.open(self.name, mode)
        return self
