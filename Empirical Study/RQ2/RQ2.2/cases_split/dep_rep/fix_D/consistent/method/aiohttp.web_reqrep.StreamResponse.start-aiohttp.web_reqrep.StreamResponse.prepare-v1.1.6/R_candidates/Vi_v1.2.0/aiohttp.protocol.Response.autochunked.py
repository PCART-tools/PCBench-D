    def autochunked(self):
        return (self.length is None and
                self._version >= HttpVersion11)
