    def __init__(self, stream, *,
                 use_mask=False, limit=DEFAULT_LIMIT, random=random.Random()):
        self.stream = stream
        self.writer = stream.transport
        self.use_mask = use_mask
        self.randrange = random.randrange
        self._closing = False
        self._limit = limit
        self._output_size = 0
