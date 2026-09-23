    @property
    @cacheit
    def dict(self):
        return {self.succ: self.p, self.fail: 1 - self.p}
