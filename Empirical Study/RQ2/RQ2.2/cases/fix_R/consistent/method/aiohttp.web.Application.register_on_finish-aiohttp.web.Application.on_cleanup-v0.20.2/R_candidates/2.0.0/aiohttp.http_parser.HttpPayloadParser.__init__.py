    def __init__(self, payload,
                 length=None, chunked=False, compression=None,
                 code=None, method=None,
                 readall=False, response_with_body=True):
        self.payload = payload

        self._length = 0
        self._type = ParseState.PARSE_NONE
        self._chunk = ChunkState.PARSE_CHUNKED_SIZE
        self._chunk_size = 0
        self._chunk_tail = b''
        self.done = False

        # payload decompression wrapper
        if (response_with_body and compression):
            payload = DeflateBuffer(payload, compression)

        # payload parser
        if not response_with_body:
            # don't parse payload if it's not expected to be received
            self._type = ParseState.PARSE_NONE
            payload.feed_eof()
            self.done = True

        elif chunked:
            self._type = ParseState.PARSE_CHUNKED
        elif length is not None:
            self._type = ParseState.PARSE_LENGTH
            self._length = length
            if self._length == 0:
                payload.feed_eof()
                self.done = True
        else:
            if readall and code != 204:
                self._type = ParseState.PARSE_UNTIL_EOF
            elif method in ('PUT', 'POST'):
                internal_logger.warning(  # pragma: no cover
                    'Content-Length or Transfer-Encoding header is required')
                self._type = ParseState.PARSE_NONE
                payload.feed_eof()
                self.done = True

        self.payload = payload
