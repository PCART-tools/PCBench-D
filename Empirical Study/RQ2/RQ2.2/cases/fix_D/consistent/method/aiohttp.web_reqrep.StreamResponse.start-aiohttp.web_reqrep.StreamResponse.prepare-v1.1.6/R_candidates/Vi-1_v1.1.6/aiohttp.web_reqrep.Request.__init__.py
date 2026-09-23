    def __init__(self, message, payload, transport, reader, writer,
                 time_service, *,
                 secure_proxy_ssl_header=None):
        self._message = message
        self._transport = transport
        self._reader = reader
        self._writer = writer
        self._post = None
        self._post_files_cache = None

        # matchdict, route_name, handler
        # or information about traversal lookup
        self._match_info = None  # initialized after route resolving

        self._payload = payload

        self._read_bytes = None
        self._has_body = not payload.at_eof()

        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        self._time_service = time_service
        self._state = {}
        self._cache = {}
