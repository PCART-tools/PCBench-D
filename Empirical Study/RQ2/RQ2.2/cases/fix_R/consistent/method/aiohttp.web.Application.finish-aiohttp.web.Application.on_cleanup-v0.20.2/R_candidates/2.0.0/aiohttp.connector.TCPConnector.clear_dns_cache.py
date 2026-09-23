    def clear_dns_cache(self, host=None, port=None):
        """Remove specified host/port or clear all dns local cache."""
        if host is not None and port is not None:
            self._cached_hosts.pop((host, port), None)
        elif host is not None or port is not None:
            raise ValueError("either both host and port "
                             "or none of them are allowed")
        else:
            self._cached_hosts.clear()
