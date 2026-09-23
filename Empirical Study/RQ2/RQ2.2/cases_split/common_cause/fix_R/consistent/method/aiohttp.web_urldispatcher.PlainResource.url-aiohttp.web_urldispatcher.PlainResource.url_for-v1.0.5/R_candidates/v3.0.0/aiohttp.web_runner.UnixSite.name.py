    @property
    def name(self):
        scheme = 'https' if self._ssl_context else 'http'
        return '{}://unix:{}:'.format(scheme, self._path)
