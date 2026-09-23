    def __init__(
        self,
        *,
        max_connections: int = None,
        max_keepalive_connections: int = None,
        # Deprecated parameter naming, in favour of more explicit version:
        max_keepalive: int = None,
    ):
        if max_keepalive is not None:
            warnings.warn(
                "'max_keepalive' is deprecated. Use 'max_keepalive_connections'.",
                DeprecationWarning,
            )
            max_keepalive_connections = max_keepalive

        self.max_connections = max_connections
        self.max_keepalive_connections = max_keepalive_connections
