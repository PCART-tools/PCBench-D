        def __hash__(self):
            return hash((str(self), self.freq))
