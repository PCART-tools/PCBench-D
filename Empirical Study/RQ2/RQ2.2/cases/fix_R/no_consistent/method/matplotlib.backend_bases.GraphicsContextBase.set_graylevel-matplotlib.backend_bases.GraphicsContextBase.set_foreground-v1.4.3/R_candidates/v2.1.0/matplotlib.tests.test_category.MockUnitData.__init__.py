    def __init__(self, data):
        seq, locs = zip(*data)
        self.seq = list(seq)
        self.locs = list(locs)
