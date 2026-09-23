    @property
    def limit(self):
        """The limit for simultaneous connections to the same endpoint.

        Endpoints are the same if they are have equal
        (host, port, is_ssl) triple.

        If limit is None the connector has no limit.
        The default limit size is 20.
        """
        return self._limit
