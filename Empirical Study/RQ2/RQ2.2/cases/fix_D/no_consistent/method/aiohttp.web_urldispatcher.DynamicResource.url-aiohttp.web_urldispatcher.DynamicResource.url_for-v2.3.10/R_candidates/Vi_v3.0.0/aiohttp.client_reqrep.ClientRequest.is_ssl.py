    def is_ssl(self):
        return self.url.scheme in ('https', 'wss')
