    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
