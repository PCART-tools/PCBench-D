class PoolLimits:
    """
    Limits on the number of connections in a connection pool.

    **Parameters:**

    * **max_keepalive** - Allow the connection pool to maintain keep-alive connections
                       below this point.
    * **max_connections** - The maximum number of concurrent connections that may be
                       established.
    """

    def __init__(
        self,
        *,
        max_keepalive: int = None,
        max_connections: int = None,
        soft_limit: int = None,
        hard_limit: int = None,
    ):
        self.max_keepalive = max_keepalive
        self.max_connections = max_connections
        if soft_limit is not None:  # pragma: nocover
            self.max_keepalive = soft_limit
            warn_deprecated("'soft_limit' is deprecated. Use 'max_keepalive' instead.",)
        if hard_limit is not None:  # pragma: nocover
            self.max_connections = hard_limit
            warn_deprecated(
                "'hard_limit' is deprecated. Use 'max_connections' instead.",
            )

    def __eq__(self, other: typing.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.max_keepalive == other.max_keepalive
            and self.max_connections == other.max_connections
        )

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(max_keepalive={self.max_keepalive}, "
            f"max_connections={self.max_connections})"
        )
