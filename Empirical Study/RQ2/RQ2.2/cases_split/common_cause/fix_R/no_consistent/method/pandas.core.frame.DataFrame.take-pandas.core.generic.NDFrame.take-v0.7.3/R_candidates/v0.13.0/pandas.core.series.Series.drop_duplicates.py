    def drop_duplicates(self, take_last=False, inplace=False):
        """
        Return Series with duplicate values removed

        Parameters
        ----------
        take_last : boolean, default False
            Take the last observed index in a group. Default first
        inplace : boolean, default False
            If True, performs operation inplace and returns None.

        Returns
        -------
        deduplicated : Series
        """
        duplicated = self.duplicated(take_last=take_last)
        result = self[-duplicated]
        if inplace:
            return self._update_inplace(result)
        else:
            return result
