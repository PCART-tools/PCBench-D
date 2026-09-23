    def __init__(
        self,
        *,
        auth: AuthTypes = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        http2: bool = False,
        proxies: ProxiesTypes = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        limits: Limits = DEFAULT_LIMITS,
        pool_limits: Limits = None,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Dict[str, typing.List[typing.Callable]] = None,
        base_url: URLTypes = "",
        transport: httpcore.SyncHTTPTransport = None,
        app: typing.Callable = None,
        trust_env: bool = True,
    ):
        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            trust_env=trust_env,
        )

        if http2:
            try:
                import h2  # noqa
            except ImportError:  # pragma: nocover
                raise ImportError(
                    "Using http2=True, but the 'h2' package is not installed. "
                    "Make sure to install httpx using `pip install httpx[http2]`."
                ) from None

        if pool_limits is not None:
            warn_deprecated(
                "Client(..., pool_limits=...) is deprecated and will raise "
                "errors in the future. Use Client(..., limits=...) instead."
            )
            limits = pool_limits

        allow_env_proxies = trust_env and app is None and transport is None
        proxy_map = self._get_proxy_map(proxies, allow_env_proxies)

        self._transport = self._init_transport(
            verify=verify,
            cert=cert,
            http2=http2,
            limits=limits,
            transport=transport,
            app=app,
            trust_env=trust_env,
        )
        self._proxies: typing.Dict[
            URLPattern, typing.Optional[httpcore.SyncHTTPTransport]
        ] = {
            URLPattern(key): None
            if proxy is None
            else self._init_proxy_transport(
                proxy,
                verify=verify,
                cert=cert,
                http2=http2,
                limits=limits,
                trust_env=trust_env,
            )
            for key, proxy in proxy_map.items()
        }
        self._proxies = dict(sorted(self._proxies.items()))
