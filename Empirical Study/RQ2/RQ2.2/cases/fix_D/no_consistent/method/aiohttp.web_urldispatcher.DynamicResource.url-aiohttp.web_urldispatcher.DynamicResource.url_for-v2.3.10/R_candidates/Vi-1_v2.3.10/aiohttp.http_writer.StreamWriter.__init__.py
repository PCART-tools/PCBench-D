    def __init__(self, protocol, transport, loop):
        self._protocol = protocol
        self._loop = loop
        self._tcp_nodelay = False
        self._tcp_cork = False
        self._socket = transport.get_extra_info('socket')
        self._waiters = []
        self.available = True
        self.transport = transport
