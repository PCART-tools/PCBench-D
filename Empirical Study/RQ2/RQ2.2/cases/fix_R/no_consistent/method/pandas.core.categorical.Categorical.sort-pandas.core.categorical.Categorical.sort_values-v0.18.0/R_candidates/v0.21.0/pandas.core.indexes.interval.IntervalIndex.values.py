    @cache_readonly
    def values(self):
        """
        Returns the IntervalIndex's data as a numpy array of Interval
        objects (with dtype='object')
        """
        left = self.left
        right = self.right
        mask = self._isnan
        closed = self._closed

        result = np.empty(len(left), dtype=object)
        for i in range(len(left)):
            if mask[i]:
                result[i] = np.nan
            else:
                result[i] = Interval(left[i], right[i], closed)
        return result
