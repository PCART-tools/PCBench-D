    @_dispatch(min=250, max=255)
    def _malformed(self, offset):
        raise ValueError("unknown command: byte %d", 250 + offset)
