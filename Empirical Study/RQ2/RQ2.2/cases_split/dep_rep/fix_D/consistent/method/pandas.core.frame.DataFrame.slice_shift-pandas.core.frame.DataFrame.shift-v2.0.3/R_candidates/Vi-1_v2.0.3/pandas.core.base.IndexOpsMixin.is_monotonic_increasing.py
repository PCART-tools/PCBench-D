    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically increasing.

        Returns
        -------
        bool
        """
        from pandas import Index

        return Index(self).is_monotonic_increasing
