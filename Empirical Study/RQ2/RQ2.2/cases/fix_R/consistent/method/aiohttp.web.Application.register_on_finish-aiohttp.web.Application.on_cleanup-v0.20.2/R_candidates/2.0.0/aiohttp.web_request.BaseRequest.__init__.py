    def __init__(self, message, payload, protocol, writer, time_service, task,
                 *, secure_proxy_ssl_header=None, client_max_size=1024**2):
        self._message = message
        self._protocol = protocol
        self._transport = protocol.transport
        self._writer = writer

        self._payload = payload
        self._headers = message.headers
        self._method = message.method
        self._version = message.version
        self._rel_url = message.url
        self._post = None
        self._read_bytes = None

        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        self._time_service = time_service
        self._state = {}
        self._cache = {}
        self._task = task
        self._client_max_size = client_max_size
