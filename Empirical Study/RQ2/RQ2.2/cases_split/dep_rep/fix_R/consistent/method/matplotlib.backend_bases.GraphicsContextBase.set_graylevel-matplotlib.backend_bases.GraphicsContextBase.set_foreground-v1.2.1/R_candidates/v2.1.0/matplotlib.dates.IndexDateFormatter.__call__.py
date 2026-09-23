    def __call__(self, x, pos=0):
        'Return the label for time *x* at position *pos*'
        ind = int(np.round(x))
        if ind >= len(self.t) or ind <= 0:
            return ''

        dt = num2date(self.t[ind], self.tz)

        return cbook.unicode_safe(dt.strftime(self.fmt))
