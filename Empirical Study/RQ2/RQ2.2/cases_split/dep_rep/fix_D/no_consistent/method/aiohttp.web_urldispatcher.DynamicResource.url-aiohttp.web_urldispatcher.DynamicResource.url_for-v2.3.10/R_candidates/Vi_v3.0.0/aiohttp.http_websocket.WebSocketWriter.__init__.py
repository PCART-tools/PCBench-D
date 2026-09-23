    def __init__(self, protocol, transport, *,
                 use_mask=False, limit=DEFAULT_LIMIT, random=random.Random(),
                 compress=0, notakeover=False):
        self.protocol = protocol
        self.transport = transport
        self.use_mask = use_mask
        self.randrange = random.randrange
        self.compress = compress
        self.notakeover = notakeover
        self._closing = False
        self._limit = limit
        self._output_size = 0
        self._compressobj = None
