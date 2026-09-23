    def __init__(self, *, resp_factory=StreamResponse, chunk_size=256*1024):
        self._response_factory = resp_factory
        self._chunk_size = chunk_size
        if bool(os.environ.get("AIOHTTP_NOSENDFILE")):
            self._sendfile = self._sendfile_fallback
