    def __call__(self, x, pos=0):
        'Return the label for time *x* at position *pos*'
        ind = int(round(x))
        if ind >= len(self.t) or ind <= 0:
            return ''
        return num2date(self.t[ind], self.tz).strftime(self.fmt)
