    def __init__(self, type, seq=None):
        self.type = type
        if seq is not None:
            self.extend(seq)
