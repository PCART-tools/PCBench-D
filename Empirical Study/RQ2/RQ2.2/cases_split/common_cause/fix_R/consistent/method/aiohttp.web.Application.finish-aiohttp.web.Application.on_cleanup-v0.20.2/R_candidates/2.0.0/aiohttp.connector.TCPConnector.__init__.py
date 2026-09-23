    def __init__(self, *, verify_ssl=True, fingerprint=None,
                 resolve=sentinel, use_dns_cache=True,
                 family=0, ssl_context=None, local_addr=None,
                 resolver=None, keepalive_timeout=sentinel,
                 force_close=False, limit=100, limit_per_host=0, loop=None):
        super().__init__(keepalive_timeout=keepalive_timeout,
                         force_close=force_close,
                         limit=limit, limit_per_host=limit_per_host, loop=loop)

        if not verify_ssl and ssl_context is not None:
            raise ValueError(
                "Either disable ssl certificate validation by "
                "verify_ssl=False or specify ssl_context, not both.")

        self._verify_ssl = verify_ssl

        if fingerprint:
            digestlen = len(fingerprint)
            hashfunc = HASHFUNC_BY_DIGESTLEN.get(digestlen)
            if not hashfunc:
                raise ValueError('fingerprint has invalid length')
            elif hashfunc is md5 or hashfunc is sha1:
                warnings.simplefilter('always')
                warnings.warn('md5 and sha1 are insecure and deprecated. '
                              'Use sha256.',
                              DeprecationWarning, stacklevel=2)
            self._hashfunc = hashfunc
        self._fingerprint = fingerprint

        if resolver is None:
            resolver = DefaultResolver(loop=self._loop)
        self._resolver = resolver

        self._use_dns_cache = use_dns_cache
        self._cached_hosts = {}
        self._ssl_context = ssl_context
        self._family = family
        self._local_addr = local_addr
