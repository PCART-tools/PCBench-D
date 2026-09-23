    @property
    def secure(self):
        """A bool indicating if the request is handled with SSL."""
        return self.scheme == 'https'
