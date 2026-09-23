    def endStream(self):
        if self.currentstream is not None:
            self.currentstream.end()
            self.currentstream = None
