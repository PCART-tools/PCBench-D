    @property
    def limit_per_host(self):
        """The limit_per_host for simultaneous connections
        to the same endpoint.

        Endpoints are the same if they are have equal
        (host, port, is_ssl) triple.

        """
        return self._limit_per_host
