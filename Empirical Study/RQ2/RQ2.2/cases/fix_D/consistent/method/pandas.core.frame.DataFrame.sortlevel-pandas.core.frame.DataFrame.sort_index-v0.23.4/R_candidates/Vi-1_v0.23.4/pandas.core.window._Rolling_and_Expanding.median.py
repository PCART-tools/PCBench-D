    def median(self, **kwargs):
        return self._apply('roll_median_c', 'median', **kwargs)
