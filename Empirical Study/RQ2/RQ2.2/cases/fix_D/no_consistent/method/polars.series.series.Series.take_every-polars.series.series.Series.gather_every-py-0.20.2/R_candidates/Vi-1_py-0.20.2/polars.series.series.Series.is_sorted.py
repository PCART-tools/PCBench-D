    def is_sorted(self, *, descending: bool = False) -> bool:
        """
        Check if the Series is sorted.

        Parameters
        ----------
        descending
            Check if the Series is sorted in descending order

        """
        return self._s.is_sorted(descending)
