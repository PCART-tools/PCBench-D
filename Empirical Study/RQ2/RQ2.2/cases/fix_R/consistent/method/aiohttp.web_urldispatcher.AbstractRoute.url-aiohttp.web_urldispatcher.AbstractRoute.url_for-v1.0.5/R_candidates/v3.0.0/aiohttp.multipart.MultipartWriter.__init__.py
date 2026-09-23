    def __init__(self, subtype='mixed', boundary=None):
        boundary = boundary if boundary is not None else uuid.uuid4().hex
        # The underlying Payload API demands a str (utf-8), not bytes,
        # so we need to ensure we don't lose anything during conversion.
        # As a result, require the boundary to be ASCII only.
        # In both situations.

        try:
            self._boundary = boundary.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('boundary should contain ASCII only chars') \
                from None
        ctype = ('multipart/{}; boundary={}'
                 .format(subtype, self._boundary_value))

        super().__init__(None, content_type=ctype)

        self._parts = []
        self._headers = CIMultiDict()
        self._headers[CONTENT_TYPE] = self.content_type
