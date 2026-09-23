    def __init__(self, fp=None):
        if not fp:
            try:
                fp = sys.stdout.buffer
            except AttributeError:
                fp = sys.stdout
        self.fp = fp
