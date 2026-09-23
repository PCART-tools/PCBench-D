    def autochunked(self):
        return (self.length is None and
                self.version >= HttpVersion11)
