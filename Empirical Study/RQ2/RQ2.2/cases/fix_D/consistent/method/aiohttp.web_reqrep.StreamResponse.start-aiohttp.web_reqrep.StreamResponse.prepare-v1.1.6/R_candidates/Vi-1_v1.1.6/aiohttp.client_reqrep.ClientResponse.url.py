    @property
    def url(self):
        warnings.warn("Deprecated, use .url_obj",
                      DeprecationWarning,
                      stacklevel=2)
        return str(self._url_obj)
