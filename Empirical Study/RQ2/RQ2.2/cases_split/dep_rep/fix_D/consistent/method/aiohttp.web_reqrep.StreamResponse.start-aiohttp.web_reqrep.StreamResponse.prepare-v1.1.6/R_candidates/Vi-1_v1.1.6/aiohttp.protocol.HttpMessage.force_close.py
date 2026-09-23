    def force_close(self):
        self.closing = True
        self.keepalive = False
