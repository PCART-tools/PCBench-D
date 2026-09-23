    def iget(self, i: int) -> SingleArrayManager:
        """
        Return the data as a SingleArrayManager.
        """
        values = self.arrays[i]
        return SingleArrayManager([values], [self._axes[0]])
