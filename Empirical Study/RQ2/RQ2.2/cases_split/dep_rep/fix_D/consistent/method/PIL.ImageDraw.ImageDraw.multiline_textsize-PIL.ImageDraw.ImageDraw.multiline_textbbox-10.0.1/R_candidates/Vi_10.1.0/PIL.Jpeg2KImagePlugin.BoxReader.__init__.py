    def __init__(self, fp, length=-1):
        self.fp = fp
        self.has_length = length >= 0
        self.length = length
        self.remaining_in_box = -1
