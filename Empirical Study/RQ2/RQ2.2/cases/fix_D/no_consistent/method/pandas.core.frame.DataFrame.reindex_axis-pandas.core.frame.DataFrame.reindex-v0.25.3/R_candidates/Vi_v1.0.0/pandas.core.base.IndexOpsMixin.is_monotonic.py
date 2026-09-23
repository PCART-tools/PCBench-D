    @property
    def is_monotonic(self):
        """
        Return boolean if values in the object are
        monotonic_increasing.

        Returns
        -------
        bool
        """
        from pandas import Index

        return Index(self).is_monotonic
