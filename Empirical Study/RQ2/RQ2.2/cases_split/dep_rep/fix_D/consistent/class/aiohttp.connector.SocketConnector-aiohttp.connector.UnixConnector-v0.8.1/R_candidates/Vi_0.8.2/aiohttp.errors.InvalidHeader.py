class InvalidHeader(HttpBadRequest):

    def __init__(self, hdr):
        super().__init__('Invalid HTTP Header: {}'.format(hdr))
        self.hdr = hdr
