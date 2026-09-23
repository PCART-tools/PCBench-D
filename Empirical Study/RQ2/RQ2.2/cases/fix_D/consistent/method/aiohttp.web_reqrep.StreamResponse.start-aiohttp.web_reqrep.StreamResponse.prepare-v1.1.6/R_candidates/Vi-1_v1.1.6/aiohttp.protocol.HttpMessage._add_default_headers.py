    def _add_default_headers(self):
        # set the connection header
        connection = None
        if self.upgrade:
            connection = 'upgrade'
        elif not self.closing if self.keepalive is None else self.keepalive:
            if self.version == HttpVersion10:
                connection = 'keep-alive'
        else:
            if self.version == HttpVersion11:
                connection = 'close'

        if connection is not None:
            self.headers[hdrs.CONNECTION] = connection
