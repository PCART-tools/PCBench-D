    def __call__(self, x, pos=0):
        return num2date(x, self.tz).strftime(self.fmt)
