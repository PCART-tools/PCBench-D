    def __init__(self, connector, key, protocol, loop):
        self._key = key
        self._connector = connector
        self._loop = loop
        self._protocol = protocol
        self._callbacks = []

        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))
