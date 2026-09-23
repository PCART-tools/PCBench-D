    @property
    def host(self):
        warnings.warn("Deprecated, use .url_obj.host",
                      DeprecationWarning,
                      stacklevel=2)
        return self._url_obj.host
