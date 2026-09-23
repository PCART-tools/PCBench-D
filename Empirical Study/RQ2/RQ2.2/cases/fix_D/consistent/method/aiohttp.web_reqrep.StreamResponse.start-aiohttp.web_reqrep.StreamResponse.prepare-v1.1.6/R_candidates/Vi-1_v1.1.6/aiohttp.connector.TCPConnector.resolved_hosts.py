    @property
    def resolved_hosts(self):
        """The dict of (host, port) -> (ipaddr, port) pairs."""
        warnings.warn((".resolved_hosts property is deprecated, "
                       "use .cached_hosts instead"),
                      DeprecationWarning, stacklevel=2)
        return self.cached_hosts
