    @property
    def scheme(self):
        """A string representing the scheme of the request.

        'http' or 'https'.
        """
        return self.url.scheme
