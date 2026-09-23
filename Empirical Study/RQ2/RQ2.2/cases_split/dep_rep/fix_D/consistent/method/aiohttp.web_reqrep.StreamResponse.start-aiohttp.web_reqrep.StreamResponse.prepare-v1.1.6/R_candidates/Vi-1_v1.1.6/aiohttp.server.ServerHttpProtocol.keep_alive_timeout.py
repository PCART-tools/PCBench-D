    @property
    def keep_alive_timeout(self):
        warnings.warn("Use keepalive_timeout property instead",
                      DeprecationWarning,
                      stacklevel=2)
        return self._keepalive_timeout
