    def __len__(self):
        """
        return the length of the RangeIndex
        """
        return max(0, -(-(self._stop - self._start) // self._step))
