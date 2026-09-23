    def __init__(self, encoding: typing.Optional[str] = None):
        self.decoder: typing.Optional[codecs.IncrementalDecoder] = (
            None if encoding is None else codecs.getincrementaldecoder(encoding)()
        )
        self.detector = chardet.universaldetector.UniversalDetector()

        # This buffer is only needed if 'decoder' is 'None'
        # we want to trigger errors if data is getting added to
        # our internal buffer for some silly reason while
        # a decoder is discovered.
        self.buffer: typing.Optional[bytearray] = None if self.decoder else bytearray()
