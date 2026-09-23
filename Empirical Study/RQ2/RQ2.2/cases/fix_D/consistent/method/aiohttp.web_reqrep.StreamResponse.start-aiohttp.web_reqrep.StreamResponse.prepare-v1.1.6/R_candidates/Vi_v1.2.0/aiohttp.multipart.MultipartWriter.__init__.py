    def __init__(self, subtype='mixed', boundary=None):
        boundary = boundary if boundary is not None else uuid.uuid4().hex
        try:
            boundary.encode('us-ascii')
        except UnicodeEncodeError:
            raise ValueError('boundary should contains ASCII only chars')
        self.headers = CIMultiDict()
        self.headers[CONTENT_TYPE] = 'multipart/{}; boundary="{}"'.format(
            subtype, boundary
        )
        self.parts = []
