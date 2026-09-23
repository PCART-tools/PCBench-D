    def clear_resolved_hosts(self, host=None, port=None):
        """Remove specified host/port or clear all resolve cache."""
        warnings.warn((".clear_resolved_hosts() is deprecated, "
                       "use .clear_dns_cache() instead"),
                      DeprecationWarning, stacklevel=2)
        if host is not None and port is not None:
            self.clear_dns_cache(host, port)
        else:
            self.clear_dns_cache()
