    def __init__(self, message, payload, protocol, writer, task,
                 loop,
                 *, client_max_size=1024**2,
                 state=None,
                 scheme=None, host=None, remote=None):
        if state is None:
            state = {}
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

        self._state = state
        self._cache = {}
        self._task = task
        self._client_max_size = client_max_size
        self._loop = loop

        self._scheme = scheme
        self._host = host
        self._remote = remote
