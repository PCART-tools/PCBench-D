    def __init__(
        self,
        *,
        max_connections: int = None,
        max_keepalive_connections: int = None,
    ):
        self.max_connections = max_connections
        self.max_keepalive_connections = max_keepalive_connections
