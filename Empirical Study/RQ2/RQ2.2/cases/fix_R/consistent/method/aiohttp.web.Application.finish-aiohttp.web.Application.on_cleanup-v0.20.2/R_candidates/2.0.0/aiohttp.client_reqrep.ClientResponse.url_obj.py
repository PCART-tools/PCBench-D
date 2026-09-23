    @property
    def url_obj(self):
        warnings.warn(
            "Deprecated, use .url #1654", DeprecationWarning, stacklevel=2)
        return self._url
