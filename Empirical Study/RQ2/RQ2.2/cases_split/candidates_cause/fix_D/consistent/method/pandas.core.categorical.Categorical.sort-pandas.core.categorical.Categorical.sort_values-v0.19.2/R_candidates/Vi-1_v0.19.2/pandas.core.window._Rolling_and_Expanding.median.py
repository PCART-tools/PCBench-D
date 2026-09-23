    def median(self, how=None, **kwargs):
        if self.freq is not None and how is None:
            how = 'median'
        return self._apply('roll_median_c', 'median', how=how, **kwargs)
