    def __init__(self, boundary, headers, content):
        self.headers = headers
        self._boundary = boundary
        self._content = content
        self._at_eof = False
        length = self.headers.get(CONTENT_LENGTH, None)
        self._length = int(length) if length is not None else None
        self._read_bytes = 0
        self._unread = deque()
        self._prev_chunk = None
        self._content_eof = 0
