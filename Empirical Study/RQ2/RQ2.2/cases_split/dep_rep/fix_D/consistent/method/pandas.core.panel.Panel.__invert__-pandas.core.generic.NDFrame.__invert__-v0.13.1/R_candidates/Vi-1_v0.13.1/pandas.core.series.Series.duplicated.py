    def duplicated(self, take_last=False):
        """
        Return boolean Series denoting duplicate values

        Parameters
        ----------
        take_last : boolean, default False
            Take the last observed index in a group. Default first

        Returns
        -------
        duplicated : Series
        """
        keys = _ensure_object(self.values)
        duplicated = lib.duplicated(keys, take_last=take_last)
        return self._constructor(duplicated,
                                 index=self.index).__finalize__(self)
