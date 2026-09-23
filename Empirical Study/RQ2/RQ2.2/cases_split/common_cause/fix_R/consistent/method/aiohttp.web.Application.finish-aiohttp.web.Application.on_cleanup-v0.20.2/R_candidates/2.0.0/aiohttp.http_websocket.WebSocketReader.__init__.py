    def __init__(self, queue):
        self.queue = queue

        self._exc = None
        self._partial = []
        self._state = WSParserState.READ_HEADER

        self._opcode = None
        self._frame_fin = False
        self._frame_opcode = None
        self._frame_payload = bytearray()

        self._tail = b''
        self._has_mask = False
        self._frame_mask = None
        self._payload_length = 0
        self._payload_length_flag = 0
