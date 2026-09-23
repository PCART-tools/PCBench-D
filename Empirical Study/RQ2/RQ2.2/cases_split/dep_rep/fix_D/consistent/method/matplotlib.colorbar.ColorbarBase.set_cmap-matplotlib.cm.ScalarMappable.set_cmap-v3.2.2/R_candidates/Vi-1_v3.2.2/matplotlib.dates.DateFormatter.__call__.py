    def __call__(self, x, pos=0):
        if x == 0:
            raise ValueError('DateFormatter found a value of x=0, which is '
                             'an illegal date; this usually occurs because '
                             'you have not informed the axis that it is '
                             'plotting dates, e.g., with ax.xaxis_date()')
        return num2date(x, self.tz).strftime(self.fmt)
