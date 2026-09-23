class LineTooLong(HttpBadRequest):

    def __init__(self, line, limit='Unknown'):
        super().__init__(
            "got more than %s bytes when reading %s" % (limit, line))
