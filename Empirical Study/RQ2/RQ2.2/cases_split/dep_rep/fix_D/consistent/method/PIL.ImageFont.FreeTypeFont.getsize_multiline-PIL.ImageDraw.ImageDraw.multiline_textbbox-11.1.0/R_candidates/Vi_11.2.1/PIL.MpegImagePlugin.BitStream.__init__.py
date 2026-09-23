    def __init__(self, fp: SupportsRead[bytes]) -> None:
        self.fp = fp
        self.bits = 0
        self.bitbuffer = 0
