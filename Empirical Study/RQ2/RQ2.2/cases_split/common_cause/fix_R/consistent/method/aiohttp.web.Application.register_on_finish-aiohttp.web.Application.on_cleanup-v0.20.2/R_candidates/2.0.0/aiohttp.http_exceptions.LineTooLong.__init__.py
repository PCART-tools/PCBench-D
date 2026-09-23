    def __init__(self, line, limit='Unknown'):
        super().__init__(
            "Got more than %s bytes when reading %s." % (limit, line))
