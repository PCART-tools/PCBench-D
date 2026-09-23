    def __init__(self, encoding: typing.Optional[str] = None):
        self.decoder: typing.Optional[codecs.IncrementalDecoder] = None
        if encoding is not None:
            self.decoder = codecs.getincrementaldecoder(encoding)(errors="strict")
