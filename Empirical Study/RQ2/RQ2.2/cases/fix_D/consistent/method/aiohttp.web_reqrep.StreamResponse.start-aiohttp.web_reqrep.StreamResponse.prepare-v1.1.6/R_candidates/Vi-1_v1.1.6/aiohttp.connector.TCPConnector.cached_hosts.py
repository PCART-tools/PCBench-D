    @property
    def cached_hosts(self):
        """Read-only dict of cached DNS record."""
        return MappingProxyType(self._cached_hosts)
