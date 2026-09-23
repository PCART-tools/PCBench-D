    def __init__(self, transport, protocol, reader, loop):
        self._transport = transport
        self._protocol = protocol
        self._reader = reader
        self._loop = loop
        self._tcp_nodelay = False
        self._tcp_cork = False
        self._socket = transport.get_extra_info('socket')
