    def _init_proxy_transport(
        self,
        proxy: Proxy,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        trust_env: bool = True,
    ) -> httpcore.SyncHTTPTransport:
        ssl_context = create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)

        return httpcore.SyncHTTPProxy(
            proxy_url=proxy.url.raw,
            proxy_headers=proxy.headers.raw,
            proxy_mode=proxy.mode,
            ssl_context=ssl_context,
            max_connections=limits.max_connections,
            max_keepalive_connections=limits.max_keepalive_connections,
            keepalive_expiry=KEEPALIVE_EXPIRY,
            http2=http2,
        )
