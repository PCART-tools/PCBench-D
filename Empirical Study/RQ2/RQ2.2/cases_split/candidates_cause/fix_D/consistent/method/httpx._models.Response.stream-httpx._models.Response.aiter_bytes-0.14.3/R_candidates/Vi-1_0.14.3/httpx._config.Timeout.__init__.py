    def __init__(
        self,
        timeout: typing.Union[TimeoutTypes, UnsetType] = UNSET,
        *,
        connect: typing.Union[None, float, UnsetType] = UNSET,
        read: typing.Union[None, float, UnsetType] = UNSET,
        write: typing.Union[None, float, UnsetType] = UNSET,
        pool: typing.Union[None, float, UnsetType] = UNSET,
        # Deprecated aliases.
        connect_timeout: typing.Union[None, float, UnsetType] = UNSET,
        read_timeout: typing.Union[None, float, UnsetType] = UNSET,
        write_timeout: typing.Union[None, float, UnsetType] = UNSET,
        pool_timeout: typing.Union[None, float, UnsetType] = UNSET,
    ):
        if not isinstance(connect_timeout, UnsetType):
            warn_deprecated(
                "httpx.Timeout(..., connect_timeout=...) is deprecated and will "
                "raise errors in a future version. "
                "Use httpx.Timeout(..., connect=...) instead."
            )
            connect = connect_timeout

        if not isinstance(read_timeout, UnsetType):
            warn_deprecated(
                "httpx.Timeout(..., read_timeout=...) is deprecated and will "
                "raise errors in a future version. "
                "Use httpx.Timeout(..., write=...) instead."
            )
            read = read_timeout

        if not isinstance(write_timeout, UnsetType):
            warn_deprecated(
                "httpx.Timeout(..., write_timeout=...) is deprecated and will "
                "raise errors in a future version. "
                "Use httpx.Timeout(..., write=...) instead."
            )
            write = write_timeout

        if not isinstance(pool_timeout, UnsetType):
            warn_deprecated(
                "httpx.Timeout(..., pool_timeout=...) is deprecated and will "
                "raise errors in a future version. "
                "Use httpx.Timeout(..., pool=...) instead."
            )
            pool = pool_timeout

        if isinstance(timeout, Timeout):
            # Passed as a single explicit Timeout.
            assert connect is UNSET
            assert read is UNSET
            assert write is UNSET
            assert pool is UNSET
            self.connect = timeout.connect  # type: typing.Optional[float]
            self.read = timeout.read  # type: typing.Optional[float]
            self.write = timeout.write  # type: typing.Optional[float]
            self.pool = timeout.pool  # type: typing.Optional[float]
        elif isinstance(timeout, tuple):
            # Passed as a tuple.
            self.connect = timeout[0]
            self.read = timeout[1]
            self.write = None if len(timeout) < 3 else timeout[2]
            self.pool = None if len(timeout) < 4 else timeout[3]
        elif not (
            isinstance(connect, UnsetType)
            or isinstance(read, UnsetType)
            or isinstance(write, UnsetType)
            or isinstance(pool, UnsetType)
        ):
            self.connect = connect
            self.read = read
            self.write = write
            self.pool = pool
        else:
            if isinstance(timeout, UnsetType):
                warnings.warn(
                    "httpx.Timeout must either include a default, or set all "
                    "four parameters explicitly. Omitting the default argument "
                    "is deprecated and will raise errors in a future version.",
                    DeprecationWarning,
                )
                timeout = None
            self.connect = timeout if isinstance(connect, UnsetType) else connect
            self.read = timeout if isinstance(read, UnsetType) else read
            self.write = timeout if isinstance(write, UnsetType) else write
            self.pool = timeout if isinstance(pool, UnsetType) else pool
