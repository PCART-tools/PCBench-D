    @property
    def connection_key(self):
        return ConnectionKey(self.host, self.port, self.ssl)
