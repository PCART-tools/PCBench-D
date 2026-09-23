    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        while len(self) >= self.maxsize:
            del self[next(iter(self))]
