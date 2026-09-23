    def __init__(self, subtype='mixed', boundary=None):
        boundary = boundary if boundary is not None else uuid.uuid4().hex
        try:
            self._boundary = boundary.encode('us-ascii')
        except UnicodeEncodeError:
            raise ValueError('boundary should contains ASCII only chars')
        ctype = 'multipart/{}; boundary="{}"'.format(subtype, boundary)

        super().__init__(None, content_type=ctype)

        self._parts = []
        self._headers = CIMultiDict()
        self._headers[CONTENT_TYPE] = self.content_type
