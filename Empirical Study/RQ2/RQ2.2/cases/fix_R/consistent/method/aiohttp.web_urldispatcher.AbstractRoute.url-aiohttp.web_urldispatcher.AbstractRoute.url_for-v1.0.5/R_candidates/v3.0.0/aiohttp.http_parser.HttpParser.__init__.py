    def __init__(self, protocol=None, loop=None,
                 max_line_size=8190, max_headers=32768, max_field_size=8190,
                 timer=None, code=None, method=None, readall=False,
                 payload_exception=None,
                 response_with_body=True, read_until_eof=False,
                 auto_decompress=True):
        self.protocol = protocol
        self.loop = loop
        self.max_line_size = max_line_size
        self.max_headers = max_headers
        self.max_field_size = max_field_size
        self.timer = timer
        self.code = code
        self.method = method
        self.readall = readall
        self.payload_exception = payload_exception
        self.response_with_body = response_with_body
        self.read_until_eof = read_until_eof

        self._lines = []
        self._tail = b''
        self._upgraded = False
        self._payload = None
        self._payload_parser = None
        self._auto_decompress = auto_decompress
