    def is_open(self):
        return not (self._ext_close or self.comm._closed)
