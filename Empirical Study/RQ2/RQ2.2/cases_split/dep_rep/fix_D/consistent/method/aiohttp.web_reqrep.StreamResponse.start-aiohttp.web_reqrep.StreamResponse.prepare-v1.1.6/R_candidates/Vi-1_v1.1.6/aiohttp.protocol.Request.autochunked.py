    def autochunked(self):
        return (self.length is None and
                self.version >= HttpVersion11 and
                self.status not in (304, 204))
