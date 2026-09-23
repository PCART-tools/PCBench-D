    def __init__(self, headers, content):
        self.headers = headers
        self._boundary = ('--' + self._get_boundary()).encode()
        self._content = content
        self._last_part = None
        self._at_eof = False
        self._at_bof = True
        self._unread = []
