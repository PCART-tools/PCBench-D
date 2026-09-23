    def _init_transport(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        transport: httpcore.AsyncHTTPTransport = None,
        app: typing.Callable = None,
        trust_env: bool = True,
    ) -> httpcore.AsyncHTTPTransport:
        if transport is not None:
            return transport

        if app is not None:
            return ASGITransport(app=app)

        ssl_context = create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)

        return httpcore.AsyncConnectionPool(
            ssl_context=ssl_context,
            max_connections=limits.max_connections,
            max_keepalive_connections=limits.max_keepalive_connections,
            keepalive_expiry=KEEPALIVE_EXPIRY,
            http2=http2,
        )
