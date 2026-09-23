    def __init__(self, trace_config_ctx_factory=SimpleNamespace):
        self._on_request_start = Signal(self)
        self._on_request_end = Signal(self)
        self._on_request_exception = Signal(self)
        self._on_request_redirect = Signal(self)
        self._on_connection_queued_start = Signal(self)
        self._on_connection_queued_end = Signal(self)
        self._on_connection_create_start = Signal(self)
        self._on_connection_create_end = Signal(self)
        self._on_connection_reuseconn = Signal(self)
        self._on_dns_resolvehost_start = Signal(self)
        self._on_dns_resolvehost_end = Signal(self)
        self._on_dns_cache_hit = Signal(self)
        self._on_dns_cache_miss = Signal(self)

        self._trace_config_ctx_factory = trace_config_ctx_factory
