    @_dispatch(min=250, max=255)
    def _malformed(self, offset):
        raise ValueError(f"unknown command: byte {250 + offset}")
