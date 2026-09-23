    def __hash__(self):
        return hash((str(self), str(self.subtype), self.closed))
