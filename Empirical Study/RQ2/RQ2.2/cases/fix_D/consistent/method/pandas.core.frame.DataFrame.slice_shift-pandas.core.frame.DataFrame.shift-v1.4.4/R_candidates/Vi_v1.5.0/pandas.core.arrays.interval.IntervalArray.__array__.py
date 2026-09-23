    def __array__(self, dtype: NpDtype | None = None) -> np.ndarray:
        """
        Return the IntervalArray's data as a numpy array of Interval
        objects (with dtype='object')
        """
        left = self._left
        right = self._right
        mask = self.isna()
        closed = self.closed

        result = np.empty(len(left), dtype=object)
        for i in range(len(left)):
            if mask[i]:
                result[i] = np.nan
            else:
                result[i] = Interval(left[i], right[i], closed)
        return result
