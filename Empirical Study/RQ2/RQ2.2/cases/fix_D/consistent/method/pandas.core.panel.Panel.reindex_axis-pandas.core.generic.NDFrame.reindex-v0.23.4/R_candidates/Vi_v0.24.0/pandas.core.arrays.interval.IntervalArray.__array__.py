    def __array__(self, dtype=None):
        """
        Return the IntervalArray's data as a numpy array of Interval
        objects (with dtype='object')
        """
        left = self.left
        right = self.right
        mask = self.isna()
        closed = self._closed

        result = np.empty(len(left), dtype=object)
        for i in range(len(left)):
            if mask[i]:
                result[i] = np.nan
            else:
                result[i] = Interval(left[i], right[i], closed)
        return result
