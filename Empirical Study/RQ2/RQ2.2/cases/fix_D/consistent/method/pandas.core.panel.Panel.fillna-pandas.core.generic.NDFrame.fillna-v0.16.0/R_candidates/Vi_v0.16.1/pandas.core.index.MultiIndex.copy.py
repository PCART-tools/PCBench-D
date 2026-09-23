    def copy(self, names=None, dtype=None, levels=None, labels=None,
             deep=False, _set_identity=False):
        """
        Make a copy of this object. Names, dtype, levels and labels can be
        passed and will be set on new copy.

        Parameters
        ----------
        names : sequence, optional
        dtype : numpy dtype or pandas type, optional
        levels : sequence, optional
        labels : sequence, optional

        Returns
        -------
        copy : MultiIndex

        Notes
        -----
        In most cases, there should be no functional difference from using
        ``deep``, but if ``deep`` is passed it will attempt to deepcopy.
        This could be potentially expensive on large MultiIndex objects.
        """
        if deep:
            from copy import deepcopy
            levels = levels if levels is not None else deepcopy(self.levels)
            labels = labels if labels is not None else deepcopy(self.labels)
            names = names if names is not None else deepcopy(self.names)
        else:
            levels = self.levels
            labels = self.labels
            names = self.names
        return MultiIndex(levels=levels,
                          labels=labels,
                          names=names,
                          sortorder=self.sortorder,
                          verify_integrity=False,
                          _set_identity=_set_identity)
