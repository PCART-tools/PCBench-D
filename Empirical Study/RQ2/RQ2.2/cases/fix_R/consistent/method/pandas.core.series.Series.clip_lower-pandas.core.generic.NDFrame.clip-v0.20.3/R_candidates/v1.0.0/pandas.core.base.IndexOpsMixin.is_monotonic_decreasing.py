    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return boolean if values in the object are
        monotonic_decreasing.

        Returns
        -------
        bool
        """
        from pandas import Index

        return Index(self).is_monotonic_decreasing
