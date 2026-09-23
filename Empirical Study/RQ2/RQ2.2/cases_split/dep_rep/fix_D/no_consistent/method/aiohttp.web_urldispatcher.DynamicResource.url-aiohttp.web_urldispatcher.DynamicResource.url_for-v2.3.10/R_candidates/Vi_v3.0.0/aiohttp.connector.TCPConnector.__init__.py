    def __init__(self, *, verify_ssl=True, fingerprint=None,
                 use_dns_cache=True, ttl_dns_cache=10,
                 family=0, ssl_context=None, ssl=None, local_addr=None,
                 resolver=None, keepalive_timeout=sentinel,
                 force_close=False, limit=100, limit_per_host=0,
                 enable_cleanup_closed=False, loop=None):
        super().__init__(keepalive_timeout=keepalive_timeout,
                         force_close=force_close,
                         limit=limit, limit_per_host=limit_per_host,
                         enable_cleanup_closed=enable_cleanup_closed,
                         loop=loop)

        self._ssl = _merge_ssl_params(ssl, verify_ssl, ssl_context,
                                      fingerprint)
        if resolver is None:
            resolver = DefaultResolver(loop=self._loop)
        self._resolver = resolver

        self._use_dns_cache = use_dns_cache
        self._cached_hosts = _DNSCacheTable(ttl=ttl_dns_cache)
        self._throttle_dns_events = {}
        self._family = family
        self._local_addr = local_addr
