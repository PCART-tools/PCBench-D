    @classmethod
    def from_url(cls, url, *, encoding='latin1'):
        """Create BasicAuth from url."""
        if not isinstance(url, URL):
            raise TypeError("url should be yarl.URL instance")
        if url.user is None:
            return None
        return cls(url.user, url.password or '', encoding=encoding)
